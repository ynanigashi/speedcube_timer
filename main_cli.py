from src.timer import SpeedcubeTimer
from src.speedcube_stats import SpeedcubeStats
from src.display import SpeedcubeDisplay
from src.scramble import generate_wca_cube_scramble
from src.log_handler import SpeedcubeLogger

def main():
    timer = SpeedcubeTimer()
    stats = SpeedcubeStats()
    display = SpeedcubeDisplay()
    logger = SpeedcubeLogger()

    while True:
        display.clear()
        scramble = generate_wca_cube_scramble()
        display.show_scramble(scramble)

        if timer.results:
            display.show_results(timer.get_recent_results())
            ao5 = stats.calculate_average(timer.results, 5)
            ao12 = stats.calculate_average(timer.results, 12)
            display.show_statistics(
                stats.format_average(ao5),
                stats.format_average(ao12)
            )

        final_time = timer.start()
        timer.add_result(scramble, final_time)
        logger.save_result(final_time)

if __name__ == "__main__":
    main()