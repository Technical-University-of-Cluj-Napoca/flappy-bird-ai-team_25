import os

class ScoreManager:
    def __init__(self, filepath="highscore.txt"):
        self.filepath = filepath
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                return [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]
        except:
            return []

    def clear_scores(self):
        self.scores = []
        with open(self.filepath, "w") as f:
            f.write("")



    def save_score(self, new_score):
        self.scores.append(new_score)
        self.scores.sort(reverse=True)
        self.scores = self.scores[:3] 
        
        try:
            with open(self.filepath, "w") as f:
                for score in self.scores:
                    f.write(f"{score}\n")
        except Exception as e:
            print(f"Error saving scores: {e}")

    def get_best_score(self):
        if self.scores:
            return self.scores[0]
        return 0

    def get_top_scores(self):
        return self.scores
