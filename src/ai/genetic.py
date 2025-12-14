import random
import copy
from src.ai.brain import Perceptron

class Species:
    def __init__(self, mascot):
        self.mascot = mascot 
        self.members = [mascot]
        self.avg_fitness = 0
        self.threshold = 1.0 

    def add_member(self, brain):
        self.members.append(brain)

    def is_compatible(self, brain):
        diff = 0
        for i in range(len(self.mascot.weights)):
            diff += abs(self.mascot.weights[i] - brain.weights[i])
        return diff < self.threshold

    def calculate_average_fitness(self):
        total = sum(b.fitness for b in self.members)
        if self.members:
            self.avg_fitness = total / len(self.members)
        else:
            self.avg_fitness = 0

    def sort_members(self):
        self.members.sort(key=lambda b: b.fitness, reverse=True)

    def reset(self):
        self.members = []
        self.avg_fitness = 0

class Population:
    def __init__(self, size):
        self.size = size
        self.brains = [Perceptron() for _ in range(size)]
        self.species = []
        self.generation = 1

    def speciate(self):
        for s in self.species:
            s.reset()
        
        for brain in self.brains:
            placed = False
            for s in self.species:
                if s.is_compatible(brain):
                    s.add_member(brain)
                    placed = True
                    break
            if not placed:
                new_species = Species(brain) 
                self.species.append(new_species)
        
        self.species = [s for s in self.species if s.members]

    def evolve(self):
        self.speciate()
        
        for s in self.species:
            s.calculate_average_fitness()
            s.sort_members()
        
        self.species.sort(key=lambda s: s.avg_fitness, reverse=True)
        
        next_gen_brains = []
        
        total_avg_fitness = sum(s.avg_fitness for s in self.species)
        
        for s in self.species:
            if total_avg_fitness > 0:
                offspring_count = int((s.avg_fitness / total_avg_fitness) * self.size)
            else:
                offspring_count = 0
            
            if len(s.members) > 0:
                champion = s.members[0]
                next_gen_brains.append(self.clone(champion))
                offspring_count = max(1, offspring_count)
            for _ in range(offspring_count - 1):
                if len(s.members) > 1:
                    parent = random.choice(s.members[1:])
                else:
                    parent = s.members[0]
                
                child = self.mutate(parent)
                next_gen_brains.append(child)
        
        while len(next_gen_brains) < self.size:
             if self.species:
                 parent_species = random.choice(self.species[:3] if len(self.species) >=3 else self.species)
                 parent = random.choice(parent_species.members)
                 next_gen_brains.append(self.mutate(parent))
             else:
                 next_gen_brains.append(Perceptron())

        self.brains = next_gen_brains
        self.generation += 1
        
    def clone(self, brain):
        new_brain = Perceptron()
        new_brain.weights = copy.deepcopy(brain.weights)
        return new_brain

    def mutate(self, brain):
        new_brain = self.clone(brain)
        mutation_rate = 0.5 
        mutation_strength = 0.5 
        
        for i in range(len(new_brain.weights)):
            if random.random() < mutation_rate:
                 new_brain.weights[i] += random.uniform(-mutation_strength, mutation_strength)
        return new_brain
