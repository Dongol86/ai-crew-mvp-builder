from main import AICrew

def run_test():
    crew = AICrew()
    test_brief = """
    Project: AI-powered fitness coaching app
    Target: Health-conscious professionals
    Core features: 
    - Workout planning
    - Progress tracking
    - AI form correction
    - Nutrition guidance
    """
    
    try:
        results = crew.process_project(test_brief)
        print("\nTest Results:")
        for agent, output in results.items():
            print(f"\n{'-'*50}")
            print(f"{agent.upper()}:")
            print(f"{output}")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    run_test()