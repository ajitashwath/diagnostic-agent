import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.laptop_repair.crew import LaptopRepairCrew

def main():
    parser = argparse.ArgumentParser(
        description="Run the Laptop Repair Crew to diagnose a system problem."
    )
    parser.add_argument(
        "problem",
        type=str,
        help="A description of the laptop problem to be diagnosed."
    )
    args = parser.parse_args()

    print("================================================")
    print("=         Laptop Repair Crew Initialized       =")
    print("================================================")
    print(f"Analyzing problem: {args.problem}\n")

    try:
        repair_crew = LaptopRepairCrew(args.problem)
        result = repair_crew.run()
        print("\n\n================================================")
        print("=              Diagnosis Report              =")
        print("================================================")
        print(result)

    except Exception as e:
        print(f"\nAn error occurred during the diagnosis process: {e}")

if __name__ == "__main__":
    main()
