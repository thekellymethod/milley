import click                            # 3rd‑party → pip install click
from powerball_suite.generator.hybrid import hybrid_pick

@click.command()
@click.option("--n", default=5, help="How many picks?")
def main(n: int) -> None:
    for _ in range(n):
        print(hybrid_pick())


if __name__ == "__main__":
    main()
