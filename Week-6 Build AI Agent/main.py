"""
main.py - Interactive CLI interface for the Autonomous Travel & Packing Agent.
"""

import sys
from src.agent import TravelAgent


def main():
    print("""
======================================================================
  🌍 AUTONOMOUS TRAVEL & PACKING CONCIERGE AGENT (Week 6)
  Features: Live Geocoding, Real Weather, Wikipedia Sights, Safe File Writer
======================================================================
    """)

    try:
        agent = TravelAgent()
    except Exception as e:
        print(f"Initialization Error: {e}")
        sys.exit(1)

    # Pre-canned high-impact demo queries
    sample_queries = [
        "I am going to bangkok tomorrow to attend a business meeting for 2 weeks, so give me what should I pack and plan a refreshment idea after the meeting for the last three days.",
        "I am going to Nairobi for a 3-day safari. What should I pack?",
        "I am visiting Addis Ababa for 2 days of relaxation. Suggest peaceful sights and what light clothes to bring."
    ]

    print("Choose an option:")
    print("  1. Run the Bangkok Business + 3-Day Refreshment scenario (Default)")
    print("  2. Run the 3-day Nairobi Safari scenario")
    print("  3. Run the Addis Ababa 2-day relaxation scenario")
    print("  4. Enter a custom travel request\n")

    choice = input("Enter choice (1-4) [default: 1]: ").strip()

    if choice == "2":
        user_prompt = sample_queries[1]
    elif choice == "3":
        user_prompt = sample_queries[2]
    elif choice == "4":
        user_prompt = input("\nEnter your travel request: ").strip()
        if not user_prompt:
            print("Empty request. Exiting.")
            return
    else:
        user_prompt = sample_queries[0]

    # Run the ReAct Agent Loop
    final_response = agent.run(user_prompt)

    print("\n" + "="*70)
    print("📋 FINAL AGENT SUMMARY:")
    print("="*70)
    print(final_response)
    print("\n💡 Note: The complete markdown travel guide has been exported to the `outputs/` folder!\n")


if __name__ == "__main__":
    main()