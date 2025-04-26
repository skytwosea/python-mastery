from pathlib import Path

def portfolio_cost(portfolio: Path) -> float:
    assert portfolio.exists()
    total = 0
    try:
        with portfolio.open(mode="r") as f:
            for line in f.readlines():
                data = line.split()[1:]
                total += float(data[0]) * float(data[1])
    except ValueError as e:
        raise SystemExit(f"bad news: {e}")
    return total

if __name__ == "__main__":
    src = Path("Data/portfolio.dat")
    print(portfolio_cost(src))
