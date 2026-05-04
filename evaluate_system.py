import time
import os
from src.recommender import load_songs, recommend_songs

def run_evaluation():
    print("Starting AI Reliability & Guardrail Evaluation...\n")
    
    # Safely load your song data
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "songs.csv")
    try:
        songs = load_songs(data_path)
    except Exception as e:
        print(f"CRITICAL ERROR: Could not load songs.csv. {e}")
        return

    # Test cases mapped to your expected dictionary format
    test_cases = [
        {
            "scenario": "Standard Request (High-Energy Pop)", 
            "input": {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False}
        },
        {
            "scenario": "Edge Case (Conflicting: Chill Mood but High Energy)", 
            "input": {"genre": "lofi", "mood": "chill", "energy": 0.90, "likes_acoustic": False}
        },
        {
            "scenario": "Vague Request (Missing Genre/Mood)", 
            "input": {"energy": 0.5} # Testing how the system handles missing keys
        }
    ]
    
    passed = 0
    failed = 0
    
    for idx, test in enumerate(test_cases):
        print(f"--- Running Test {idx+1}: {test['scenario']} ---")
        print(f"Input Profile: {test['input']}")
        
        try:
            # ACTUAL API CALL TO YOUR CODE
            response = recommend_songs(test['input'], songs, k=2)
            
            # Format the output clearly
            if response:
                top_song = response[0][0] # The dictionary of the #1 song
                explanation = response[0][2] # The reasoning string
                output_str = f"'{top_song['title']}' by {top_song['artist']} (Why: {explanation})"
            else:
                output_str = "No recommendations returned."
                
            print(f"Output: {output_str}\n")
            
            # Validation: Pass if it successfully returns a list with items
            if isinstance(response, list) and len(response) > 0:
                print("Status: PASS (Valid recommendations generated)\n")
                passed += 1
            else:
                print("Status: FAIL (Empty or invalid response)\n")
                failed += 1
                
        except Exception as e:
            print(f"Status: FAIL (System crashed or errored: {e})\n")
            failed += 1
            
        time.sleep(1)
            
    # Final Report
    print("===================================")
    print("    EVALUATION SUMMARY REPORT      ")
    print("===================================")
    print(f"Total Tests Run: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    confidence_score = (passed / len(test_cases)) * 100
    print(f"Overall System Reliability Score: {confidence_score:.1f}%")

if __name__ == "__main__":
    run_evaluation()