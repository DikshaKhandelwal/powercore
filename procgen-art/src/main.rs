use clap::{Parser, Subcommand};
use crossterm::{cursor, execute, style::{Color, Print, ResetColor, SetBackgroundColor}, terminal::{Clear, ClearType, EnterAlternateScreen, LeaveAlternateScreen, disable_raw_mode, enable_raw_mode}};
use indicatif::{ProgressBar, ProgressStyle};
use rand::{rngs::StdRng, Rng, SeedableRng};
use serde::Serialize;
use std::{cmp::min, io::{stdout, Write}, thread, time::Duration};
use sysinfo::{CpuExt, DiskExt, NetworkExt, System, SystemExt};

const LINE_LIMIT: usize = 500;

#[derive(Parser)]
#[command(name = "procgen-art", about = "Terminal generative art driven by system metrics", version)]
struct Args {
    #[arg(long, default_value_t = 500, help = "Frame interval in milliseconds"]
    interval: u64,
    #[arg(long, default_value = "plasma", value_parser = ["plasma", "waves", "ember"], help = "Art style")]
    style: String,
    #[arg(long, help = "Render once and exit")]
    once: bool,
    #[arg(long, help = "Output JSON snapshot instead of live art")]
    json: bool,
    #[arg(long, default_value_t = 80, help = "Width of canvas")]
    width: u16,
    #[arg(long, default_value_t = 24, help = "Height of canvas")]
    height: u16,
    #[arg(long, help = "Seed override for deterministic art")]
    seed: Option<u64>,
    #[arg(long, help = "Enforce 500-line executable budget")]
    strict: bool,
}

#[derive(Subcommand)]
enum Command {
    #[command(about = "Launch the generative art canvas")]
    Run,
    #[command(about = "Print current system metrics in JSON")]
    Metrics,
}

#[derive(Serialize, Clone)]
struct Metrics {
    cpu_usage: f32,
    load_avg: f64,
    total_memory: u64,
    used_memory: u64,
    disk_usage: Vec<DiskMetrics>,
    network_rx: u64,
    network_tx: u64,
    entropy: u64,
}

#[derive(Serialize, Clone)]
struct DiskMetrics {
    name: String,
    total_space: u64,
    available_space: u64,
}

#[derive(Serialize)]
struct Snapshot {
    metrics: Metrics,
    frame: Vec<String>,
    width: u16,
    height: u16,
    style: String,
}

fn ensure_line_budget() {
    if count_executable_lines(include_str!("main.rs")) > LINE_LIMIT {
        eprintln!("warning: executable lines exceeded {}", LINE_LIMIT);
        std::process::exit(3);
    }
}

fn count_executable_lines(source: &str) -> usize {
    source
        .lines()
        .filter(|line| {
            let trimmed = line.trim();
            !trimmed.is_empty() && !trimmed.starts_with("//")
        })
        .count()
}

fn gather_metrics(sys: &mut System) -> Metrics {
    sys.refresh_cpu();
    sys.refresh_memory();
    sys.refresh_disks_list();
    sys.refresh_networks();

    let cpu_usage = sys.global_cpu_info().cpu_usage();
    let load_avg = sys.load_average().one;
    let total_memory = sys.total_memory();
    let used_memory = sys.used_memory();
    let network_rx = sys
        .networks()
        .values()
        .map(|data| data.received())
        .sum();
    let network_tx = sys
        .networks()
        .values()
        .map(|data| data.transmitted())
        .sum();
    let disk_usage = sys
        .disks()
        .iter()
        .map(|disk| DiskMetrics {
            name: disk.name().to_string_lossy().to_string(),
            total_space: disk.total_space(),
            available_space: disk.available_space(),
        })
        .collect();

    let entropy = (cpu_usage * 100.0) as u64
        + used_memory
        + network_rx
        + network_tx
        + disk_usage.iter().map(|disk| disk.total_space()).sum::<u64>();

    Metrics {
        cpu_usage,
        load_avg,
        total_memory,
        used_memory,
        disk_usage,
        network_rx,
        network_tx,
        entropy,
    }
}

fn palette(style: &str) -> Vec<Color> {
    match style {
        "waves" => vec![Color::Blue, Color::Cyan, Color::Black],
        "ember" => vec![Color::DarkRed, Color::Red, Color::DarkYellow, Color::Yellow],
        _ => vec![Color::Magenta, Color::DarkMagenta, Color::Blue, Color::Black],
    }
}

fn art_char(style: &str, intensity: f32) -> char {
    let ramps = match style {
        "waves" => " .-~*~=",
        "ember" => "`^";",
        _ => " .:+*#%@",
    };
    let idx = ((intensity.clamp(0.0, 1.0)) * (ramps.len() as f32 - 1.0)).round() as usize;
    ramps.chars().nth(min(idx, ramps.len() - 1)).unwrap_or('*')
}

fn render_frame(metrics: &Metrics, rng: &mut StdRng, width: u16, height: u16, style: &str) -> Vec<String> {
    let colors = palette(style);
    let mut frame = Vec::with_capacity(height as usize);
    let cpu = metrics.cpu_usage / 100.0;
    let memory = metrics.used_memory as f32 / metrics.total_memory as f32;
    let network = ((metrics.network_rx + metrics.network_tx) as f32).ln().max(0.0) / 15.0;
    let base_seed = metrics.entropy;

    for y in 0..height {
        let mut row = String::with_capacity(width as usize);
        for x in 0..width {
            let noise = rng.gen::<f32>();
            let swirl = ((x as f32 / width as f32) * cpu + (y as f32 / height as f32) * memory + noise * network).sin();
            let intensity = ((swirl + 1.0) / 2.0 * memory + cpu).fract();
            row.push(art_char(style, intensity));
        }
        frame.push(row);
    }

    let mut overlay = frame.clone();
    if !overlay.is_empty() {
        let text = format!(
            "CPU {:>5.1}% | MEM {:>5.1}% | NET {:>7.1}k/s",
            metrics.cpu_usage,
            memory * 100.0,
            (metrics.network_rx + metrics.network_tx) as f32 / 1024.0
        );
        let y = (height / 2) as usize;
        let start = if text.len() < width as usize {
            (width as usize - text.len()) / 2
        } else {
            0
        };
        if y < overlay.len() {
            let line = &mut overlay[y];
            for (i, ch) in text.chars().enumerate() {
                if start + i < line.len() {
                    line.replace_range(start + i..start + i + 1, &ch.to_string());
                }
            }
        }
    }

    if base_seed % 7 == 0 && !overlay.is_empty() {
        overlay[0] = format!("Style: {style} | Frames seeded by entropy {base_seed}");
    }

    overlay
}

fn display_frame(frame: &[String], style: &str) -> crossterm::Result<()> {
    execute!(stdout(), cursor::MoveTo(0, 0), Clear(ClearType::All))?;
    let colors = palette(style);
    for (idx, line) in frame.iter().enumerate() {
        let color = colors[idx % colors.len()];
        execute!(
            stdout(),
            SetBackgroundColor(color),
            cursor::MoveTo(0, idx as u16),
            Print(line),
            ResetColor
        )?;
    }
    stdout().flush()?;
    Ok(())
}

fn snapshot(metrics: Metrics, frame: Vec<String>, width: u16, height: u16, style: &str) {
    let payload = Snapshot {
        metrics,
        frame,
        width,
        height,
        style: style.to_string(),
    };
    println!("{}", serde_json::to_string_pretty(&payload).unwrap());
}

fn run_live(args: &Args) -> crossterm::Result<()> {
    let mut sys = System::new_all();
    let mut rng = match args.seed {
        Some(seed) => StdRng::seed_from_u64(seed),
        None => StdRng::seed_from_u64(gather_metrics(&mut sys).entropy),
    };
    enable_raw_mode()?;
    execute!(stdout(), EnterAlternateScreen)?;
    let mut spinner = ProgressBar::new_spinner();
    spinner.set_style(ProgressStyle::with_template("{spinner:.green} {msg}").unwrap());
    spinner.set_message("Generating art...");

    loop {
        let metrics = gather_metrics(&mut sys);
        let frame = render_frame(&metrics, &mut rng, args.width, args.height, &args.style);
        display_frame(&frame, &args.style)?;
        spinner.tick();
        if args.once {
            snapshot(metrics, frame, args.width, args.height, &args.style);
            break;
        }
        thread::sleep(Duration::from_millis(args.interval));
    }

    spinner.finish_and_clear();
    execute!(stdout(), LeaveAlternateScreen)?;
    disable_raw_mode()?;
    Ok(())
}

fn run_snapshot(args: &Args) -> crossterm::Result<()> {
    let mut sys = System::new_all();
    let mut rng = match args.seed {
        Some(seed) => StdRng::seed_from_u64(seed),
        None => StdRng::seed_from_u64(gather_metrics(&mut sys).entropy),
    };
    let metrics = gather_metrics(&mut sys);
    let frame = render_frame(&metrics, &mut rng, args.width, args.height, &args.style);
    snapshot(metrics, frame, args.width, args.height, &args.style);
    Ok(())
}

fn run_metrics() {
    let mut sys = System::new_all();
    let metrics = gather_metrics(&mut sys);
    println!("{}", serde_json::to_string_pretty(&metrics).unwrap());
}

fn main() {
    let args = Args::parse();
    ensure_line_budget();
    if args.strict {
        ensure_line_budget();
    }
    if args.json {
        if let Err(err) = run_snapshot(&args) {
            eprintln!("error: {err}");
            std::process::exit(2);
        }
        return;
    }
    if let Err(err) = run_live(&args) {
        eprintln!("error: {err}");
        let _ = execute!(stdout(), LeaveAlternateScreen);
        let _ = disable_raw_mode();
        std::process::exit(2);
    }
}
