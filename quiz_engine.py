import json
import random
import time
from datetime import datetime
from typing import List, Dict, Any

class QuizEngine:
    def __init__(self):
        self.questions = self._load_questions()
        self.user_stats = {
            'total_games': 0,
            'total_score': 0,
            'best_score': 0,
            'average_score': 0,
            'categories_played': set(),
            'total_time_played': 0,
            'streak': 0,
            'best_streak': 0
        }
        
    def _load_questions(self) -> Dict[str, List[Dict]]:
        """Load quiz questions by category"""
        return {
            "Python Programming": [
                {
                    "question": "What is the output of print(type([]))?",
                    "options": ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"],
                    "correct": 0,
                    "difficulty": "easy",
                    "explanation": "[] creates a list object, so type([]) returns <class 'list'>"
                },
                {
                    "question": "Which method is used to add an element to a set?",
                    "options": ["append()", "add()", "insert()", "push()"],
                    "correct": 1,
                    "difficulty": "easy",
                    "explanation": "Sets use the add() method to add elements"
                },
                {
                    "question": "What does the 'yield' keyword do in Python?",
                    "options": ["Returns a value", "Creates a generator", "Stops execution", "Imports a module"],
                    "correct": 1,
                    "difficulty": "medium",
                    "explanation": "yield creates a generator function that can pause and resume execution"
                },
                {
                    "question": "What is a decorator in Python?",
                    "options": ["A design pattern", "A function that modifies another function", "A data type", "A loop structure"],
                    "correct": 1,
                    "difficulty": "medium",
                    "explanation": "Decorators are functions that modify or extend other functions"
                },
                {
                    "question": "What is the Global Interpreter Lock (GIL)?",
                    "options": ["A security feature", "A mutex that protects Python objects", "A compilation step", "A memory manager"],
                    "correct": 1,
                    "difficulty": "hard",
                    "explanation": "GIL is a mutex that prevents multiple threads from executing Python bytecode simultaneously"
                }
            ],
            "Data Science": [
                {
                    "question": "What does pandas DataFrame.groupby() return?",
                    "options": ["DataFrame", "Series", "GroupBy object", "List"],
                    "correct": 2,
                    "difficulty": "medium",
                    "explanation": "groupby() returns a GroupBy object that can be used for aggregation operations"
                },
                {
                    "question": "Which library is primarily used for numerical computing in Python?",
                    "options": ["Pandas", "NumPy", "Matplotlib", "Scikit-learn"],
                    "correct": 1,
                    "difficulty": "easy",
                    "explanation": "NumPy is the fundamental library for numerical computing in Python"
                },
                {
                    "question": "What is overfitting in machine learning?",
                    "options": ["Model performs well on training data but poorly on test data", "Model is too simple", "Model has too few parameters", "Model trains too fast"],
                    "correct": 0,
                    "difficulty": "medium",
                    "explanation": "Overfitting occurs when a model learns the training data too well, including noise"
                }
            ],
            "Web Development": [
                {
                    "question": "What does HTTP stand for?",
                    "options": ["HyperText Transfer Protocol", "High Tech Transfer Protocol", "HyperText Transport Protocol", "High Transfer Text Protocol"],
                    "correct": 0,
                    "difficulty": "easy",
                    "explanation": "HTTP stands for HyperText Transfer Protocol"
                },
                {
                    "question": "Which HTTP status code indicates 'Not Found'?",
                    "options": ["200", "404", "500", "301"],
                    "correct": 1,
                    "difficulty": "easy",
                    "explanation": "404 is the standard HTTP status code for 'Not Found'"
                },
                {
                    "question": "What is REST in web development?",
                    "options": ["A programming language", "An architectural style for web services", "A database", "A framework"],
                    "correct": 1,
                    "difficulty": "medium",
                    "explanation": "REST (Representational State Transfer) is an architectural style for designing web services"
                }
            ],
            "General Knowledge": [
                {
                    "question": "What is the capital of Australia?",
                    "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                    "correct": 2,
                    "difficulty": "medium",
                    "explanation": "Canberra is the capital city of Australia"
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                    "correct": 1,
                    "difficulty": "easy",
                    "explanation": "Mars is called the Red Planet due to its reddish appearance"
                },
                {
                    "question": "Who painted the Mona Lisa?",
                    "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
                    "correct": 2,
                    "difficulty": "easy",
                    "explanation": "The Mona Lisa was painted by Leonardo da Vinci"
                }
            ]
        }

    def get_categories(self) -> List[str]:
        """Get all available quiz categories"""
        return list(self.questions.keys())

    def start_quiz(self, category: str, num_questions: int = 5) -> Dict[str, Any]:
        """Start a new quiz session"""
        if category not in self.questions:
            return {"error": "Category not found"}
        
        available_questions = self.questions[category].copy()
        if len(available_questions) < num_questions:
            num_questions = len(available_questions)
        
        selected_questions = random.sample(available_questions, num_questions)
        
        quiz_session = {
            "category": category,
            "questions": selected_questions,
            "current_question": 0,
            "score": 0,
            "start_time": time.time(),
            "answers": [],
            "total_questions": num_questions
        }
        
        return quiz_session

    def answer_question(self, quiz_session: Dict, answer_index: int) -> Dict[str, Any]:
        """Process an answer and return result"""
        current_q = quiz_session["current_question"]
        question = quiz_session["questions"][current_q]
        
        is_correct = answer_index == question["correct"]
        
        answer_result = {
            "correct": is_correct,
            "correct_answer": question["correct"],
            "explanation": question["explanation"],
            "difficulty": question["difficulty"]
        }
        
        quiz_session["answers"].append(answer_result)
        
        if is_correct:
            quiz_session["score"] += 1
            if question["difficulty"] == "easy":
                quiz_session["score"] += 1
            elif question["difficulty"] == "medium":
                quiz_session["score"] += 2
            elif question["difficulty"] == "hard":
                quiz_session["score"] += 3
        
        quiz_session["current_question"] += 1
        
        return answer_result

    def finish_quiz(self, quiz_session: Dict) -> Dict[str, Any]:
        """Finish quiz and calculate final results"""
        end_time = time.time()
        time_taken = end_time - quiz_session["start_time"]
        
        correct_answers = sum(1 for answer in quiz_session["answers"] if answer["correct"])
        total_questions = quiz_session["total_questions"]
        percentage = (correct_answers / total_questions) * 100
        
        # Update user stats
        self.user_stats["total_games"] += 1
        self.user_stats["total_score"] += quiz_session["score"]
        self.user_stats["categories_played"].add(quiz_session["category"])
        self.user_stats["total_time_played"] += time_taken
        
        if quiz_session["score"] > self.user_stats["best_score"]:
            self.user_stats["best_score"] = quiz_session["score"]
        
        self.user_stats["average_score"] = self.user_stats["total_score"] / self.user_stats["total_games"]
        
        # Calculate streak
        if percentage >= 80:  # 80% or higher continues streak
            self.user_stats["streak"] += 1
            if self.user_stats["streak"] > self.user_stats["best_streak"]:
                self.user_stats["best_streak"] = self.user_stats["streak"]
        else:
            self.user_stats["streak"] = 0
        
        results = {
            "score": quiz_session["score"],
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "percentage": percentage,
            "time_taken": time_taken,
            "category": quiz_session["category"],
            "difficulty_breakdown": self._get_difficulty_breakdown(quiz_session["answers"]),
            "performance_level": self._get_performance_level(percentage),
            "user_stats": self.user_stats.copy()
        }
        
        return results

    def _get_difficulty_breakdown(self, answers: List[Dict]) -> Dict[str, Dict]:
        """Get breakdown of performance by difficulty"""
        breakdown = {"easy": {"correct": 0, "total": 0}, 
                    "medium": {"correct": 0, "total": 0}, 
                    "hard": {"correct": 0, "total": 0}}
        
        for answer in answers:
            difficulty = answer["difficulty"]
            breakdown[difficulty]["total"] += 1
            if answer["correct"]:
                breakdown[difficulty]["correct"] += 1
        
        return breakdown

    def _get_performance_level(self, percentage: float) -> str:
        """Get performance level based on percentage"""
        if percentage >= 90:
            return "Excellent! 🏆"
        elif percentage >= 80:
            return "Great! 🌟"
        elif percentage >= 70:
            return "Good! 👍"
        elif percentage >= 60:
            return "Fair 📚"
        else:
            return "Keep Learning! 💪"

    def get_leaderboard(self) -> List[Dict]:
        """Get leaderboard (simulated for demo)"""
        return [
            {"name": "You", "score": self.user_stats["best_score"], "games": self.user_stats["total_games"]},
            {"name": "Alice", "score": 245, "games": 15},
            {"name": "Bob", "score": 230, "games": 12},
            {"name": "Charlie", "score": 220, "games": 18},
            {"name": "Diana", "score": 210, "games": 10}
        ]

# Demo the quiz engine
def demo_quiz():
    print("🎯 Welcome to the Advanced Quiz Engine!")
    print("=" * 50)
    
    quiz = QuizEngine()
    
    # Show available categories
    categories = quiz.get_categories()
    print(f"📚 Available Categories: {', '.join(categories)}")
    print()
    
    # Start a demo quiz
    category = "Python Programming"
    print(f"🚀 Starting {category} Quiz...")
    quiz_session = quiz.start_quiz(category, 3)
    
    # Simulate answering questions
    demo_answers = [0, 1, 0]  # Some correct, some incorrect
    
    for i in range(quiz_session["total_questions"]):
        question = quiz_session["questions"][i]
        print(f"\n❓ Question {i+1}: {question['question']}")
        print(f"   Difficulty: {question['difficulty'].upper()}")
        
        for j, option in enumerate(question['options']):
            print(f"   {j+1}. {option}")
        
        # Simulate answer
        answer = demo_answers[i] if i < len(demo_answers) else 0
        print(f"   👤 Your answer: {answer + 1}")
        
        result = quiz.answer_question(quiz_session, answer)
        
        if result["correct"]:
            print("   ✅ Correct!")
        else:
            print(f"   ❌ Wrong! Correct answer: {result['correct_answer'] + 1}")
        print(f"   💡 {result['explanation']}")
    
    # Finish quiz and show results
    final_results = quiz.finish_quiz(quiz_session)
    
    print("\n" + "=" * 50)
    print("🏁 QUIZ COMPLETED!")
    print("=" * 50)
    print(f"📊 Final Score: {final_results['score']} points")
    print(f"✅ Correct Answers: {final_results['correct_answers']}/{final_results['total_questions']}")
    print(f"📈 Percentage: {final_results['percentage']:.1f}%")
    print(f"⏱️  Time Taken: {final_results['time_taken']:.1f} seconds")
    print(f"🎭 Performance: {final_results['performance_level']}")
    
    print(f"\n🔥 Current Streak: {final_results['user_stats']['streak']}")
    print(f"🏆 Best Score: {final_results['user_stats']['best_score']}")
    print(f"📊 Average Score: {final_results['user_stats']['average_score']:.1f}")
    
    # Show difficulty breakdown
    print("\n📈 Performance by Difficulty:")
    for difficulty, stats in final_results['difficulty_breakdown'].items():
        if stats['total'] > 0:
            percentage = (stats['correct'] / stats['total']) * 100
            print(f"   {difficulty.capitalize()}: {stats['correct']}/{stats['total']} ({percentage:.0f}%)")
    
    # Show leaderboard
    print("\n🏆 Leaderboard:")
    leaderboard = quiz.get_leaderboard()
    for i, player in enumerate(leaderboard[:5], 1):
        emoji = "👑" if i == 1 else f"{i}️⃣"
        print(f"   {emoji} {player['name']}: {player['score']} points ({player['games']} games)")

# Run the demo
demo_quiz()
