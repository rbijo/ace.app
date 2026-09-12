class MotivationService:

    @staticmethod
    def get_encouragement_message(percentage: float, completed_count: int) -> str:
        if percentage >= 100.0:
            return "🎉 Outstanding! You have mastered 100% of this subject's flowchart roadmap!"
        elif percentage >= 75.0:
            return "🚀 Fantastic progress! You're in the final homestretch with over 75% completed!"
        elif percentage >= 50.0:
            return "💪 Over halfway there! Keep up the great momentum across your study nodes."
        elif percentage > 0.0:
            return f"🌱 Great start! You've completed {completed_count} topics ({percentage}%). Keep going!"
        else:
            return "🎯 Ready to learn? Select your first topic node on the roadmap to begin!"

