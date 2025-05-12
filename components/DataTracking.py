import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pygame
from pathlib import Path

class DataTracking:
    
    def __init__(self, SlimeManager):
        self.data = pd.DataFrame()
        self.SlimeManager = SlimeManager
        self.score = SlimeManager.score
        self.total_score = 0
        self.current_score = []
        self.max_combo = 0
        self.score_type = [0, 0, 0, 0] # [perfect, good, ok, miss]
        self.timing = []
        self.accuracy = []
        self.beat = []
        self.average_timing = 0
        self.average_accuracy = 0

    def newRecord(self, mapName, score):
        # example score with (points, time accuracy, beat, position accuracy)
        # [(300, 0.09399999999999986, 2, 0.9996052315952038), (100, 0.21399999999999997, 3, 0.995776256916692), (100, 0.399, 4, 0.23069444316796028), (100, 0.2190000000000003, 4, 0.9990989316831599), (300, 0.02200000000000024, 5, 0.7365714540537598), (300, 0.05600000000000005, 5, 0.9058911009004299), (300, 0.03000000000000025, 5.5, 0.9184126076), (300, 0.0030000000000001137, 5.5, 0.9896641922207601), (300, 0.0030000000000001137, 6, 0.9867961058010626), (300, 0.03699999999999992, 6, 0.98848113357756), (300, 0.07000000000000028, 6, 0.9948188796), (100, 0.33399999999999963, 7, 0.050200053298563585), (300, 0.04999999999999982, 7, 0.15339974999999995), (300, 0.08399999999999963, 7, 0.4374827634585595), (300, 0.0389999999999997, 8, 0.009294921126359657), (300, 0.0259999999999998, 9, 0.42045761602495946), (300, 0.07399999999999984, 9, 0.33678140124095934), (300, 0.09299999999999997, 9.5, 0.9648414199135141), (300, 0.025000000000000355, 10, 0.7870065670197067), (300, 0.045999999999999375, 11, 0.8903909771257595), (300, 0.0470000000000006, 11.5, 0.9965950674367601), (300, 0.0470000000000006, 12, 0.9600804987347701), (300, 0.06400000000000006, 12, 0.97888734897643), (300, 0.057000000000000384, 13, 0.4826822496639599), (300, 0.08999999999999986, 13, 0.6250596155999989), (100, 0.14199999999999946, 14, 0.8451157145081598), (100, 0.15799999999999947, 14, 0.9997439347254475), (300, 0.02800000000000047, 15, 0.5049021204377602), (300, 0.062000000000001165, 16, 0.38223649669056137), (300, 0.09499999999999886, 16, 0.7859474781992186), (300, 0.019999999999999574, 17, 0.9772550336), (300, 0.036999999999999034, 17, 0.33393090957755955), (300, 0.03999999999999915, 17.5, 0.9912901375999998), (300, 0.07400000000000162, 17.5, 0.9999405353291956), (300, 0.012000000000000455, 18, 0.6715546165145603), (300, 0.045999999999999375, 18, 0.9359718731257605), (300, 0.0799999999999983, 18, 0.9940809717571116)]
        combo = 0
        for s in score:
            self.beat.append(s[2])
            self.total_score += s[0]
            self.current_score.append(s[0])
            self.timing.append(100 - math.fabs(round(s[1] * 100)))
            self.accuracy.append(round(s[3] * 100))
            self.average_accuracy = np.mean(self.accuracy)
            self.average_timing = np.mean(self.timing)
            self.score_type[0] += 1 if s[0] == 300 else 0
            self.score_type[1] += 1 if s[0] == 100 else 0
            self.score_type[2] += 1 if s[0] == 50 else 0
            self.score_type[3] += 1 if s[0] == 0 else 0
            if s[0] != 0:
                combo += 1
            else:
                if combo > self.max_combo:
                    self.max_combo = combo
                combo = 0
        if combo > self.max_combo:
            self.max_combo = combo
        # average accuracy
        # average timing
        self.average_accuracy = np.mean(self.accuracy)
        self.average_timing = np.mean(self.timing)
        
        self.save_score(mapName)


    def save_score(self, mapName):
        # Create new record
        new_record = {
            "total_score": self.total_score,
            "current_score": self.current_score,
            "max_combo": self.max_combo,
            "accuracy": self.accuracy,
            "timing": self.timing,
            "average_accuracy": self.average_accuracy,
            "average_timing": self.average_timing,
            "beat": self.beat,
            "song": mapName,
            "player": "Player",
            "score_type": {
                "perfect": self.score_type[0],
                "good": self.score_type[1],
                "ok": self.score_type[2],
                "miss": self.score_type[3]
            }
        }
        
        # Path to JSON file
        json_path = Path("data.json")
        
        # Load existing data or initialize empty list
        if json_path.exists():
            with open(json_path, 'r') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        
        # Append new record
        existing_data.append(new_record)
        
        # Save back to file
        with open(json_path, 'w') as f:
            json.dump(existing_data, f, indent=2)  # indent for pretty-printing

    def generate_visualizations(self):
        figures = []
        
        # 1. Accuracy Over Time (Line Graph) - Wider and taller
        fig1 = plt.figure(figsize=(8, 8))
        plt.plot(self.beat, self.accuracy, 'b-', linewidth=2, label='Accuracy')
        plt.title('Accuracy Over Time', pad=20)
        plt.ylabel('Accuracy (%)', labelpad=10)
        plt.ylim(0, 100)  # Ensure y-axis starts at 0
        plt.grid(True, alpha=0.3)
        plt.tight_layout(pad=3)
        figures.append(fig1)

        # 2. Timing Over Time (Line Graph) - Wider and taller
        fig2 = plt.figure(figsize=(12, 10))
        plt.plot(self.beat, self.timing, 'r-', linewidth=2, label='Timing')
        plt.title('Timing Over Time', pad=20)
        plt.ylabel('Timing Accuracy (%)', labelpad=10)
        plt.ylim(0, 100)  # Ensure y-axis starts at 0
        plt.grid(True, alpha=0.3)
        plt.tight_layout(pad=3)
        figures.append(fig2)
        
        # 3. Score Distribution (Bar Graph) - More compact
        fig3 = plt.figure(figsize=(8, 8))
        score_types = ['Perfect', 'Good', 'OK', 'Miss']
        colors = ['#4CAF50', '#2196F3', '#FFC107', '#F44336']
        bars = plt.bar(score_types, self.score_type, color=colors)
        plt.title('Score Distribution', pad=15)
        plt.ylabel('Count', labelpad=10)
        plt.ylim(0, max(self.score_type))  # Ensure y-axis starts at 0
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.tight_layout(pad=3)
        figures.append(fig3)
        
        # 4. Timing vs Accuracy (Scatter Plot) - Square aspect ratio
        fig4 = plt.figure(figsize=(8, 8))
        scatter = plt.scatter(
            self.beat, 
            self.timing, 
            c=self.accuracy, 
            cmap='viridis', 
            s=100, 
            alpha=0.7,
            vmin=0,  # Set minimum color limit
            vmax=100  # Set maximum color limit
        )
        plt.title('Timing vs Accuracy', pad=15)
        plt.ylabel('Timing (%)', labelpad=10)
        plt.ylim(0, 100)  # Ensure y-axis starts at 0
        cbar = plt.colorbar(scatter)
        cbar.set_label('Position Accuracy (%)', labelpad=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout(pad=3)
        figures.append(fig4)

        # 5. Enhanced stats visualization with combined labels
        fig5 = plt.figure(figsize=(8, 8))
        total_hits = len(self.score)
        perfect_score = total_hits * 300
        score_percentage = (self.total_score / perfect_score) * 100 if perfect_score > 0 else 0
        max_possible_combo = total_hits
        combo_percentage = (self.max_combo / max_possible_combo) * 100 if max_possible_combo > 0 else 0

        stats = {
            'Score': (self.total_score, score_percentage),
            'Combo': (self.max_combo, combo_percentage),
            'Timing': self.average_timing,
            'Accuracy': self.average_accuracy
        }

        colors = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']
        percent_values = [stat[1] if isinstance(stat, tuple) else stat for stat in stats.values()]
        bars = plt.barh(list(stats.keys()), percent_values, color=colors)

        plt.title('Game Statistics', pad=20, fontsize=14)
        plt.xlim(0, 100)  # Ensure x-axis starts at 0
        plt.grid(axis='x', alpha=0.3)

        # Add combined value-percentage labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            stat_name = list(stats.keys())[i]
            stat_value = stats[stat_name]
            
            if isinstance(stat_value, tuple):
                # For Score and Combo - show "value (percentage%)"
                raw_value, percentage = stat_value
                label = f"{raw_value} ({percentage:.1f}%)"

            else:
                # For Timing/Accuracy - show "percentage%"
                label = f"{stat_value:.1f}%"
            
            # Position label inside bar (centered vertically, left-aligned)
            text_x = min(width * 0.15, 5)  # Left-aligned with small margin
            plt.text(text_x, bar.get_y() + bar.get_height()/2,
                    label,
                    ha='left', va='center',
                    color='white', fontweight='bold',
                    fontsize=10)

        plt.tight_layout(pad=2)
        figures.append(fig5)
            

        # 6. Cumulative Score Over Time (Line Graph) - Wider and taller
        fig6 = plt.figure(figsize=(8, 8))
        cumulative_score = np.cumsum(self.current_score)
        plt.plot(self.beat, cumulative_score, 'g-', linewidth=2, label='Cumulative Score')
        plt.title('Cumulative Score Over Time', pad=20)
        plt.ylim(0, max(cumulative_score))  # Ensure y-axis starts at 0
        figures.append(fig6)
        
        return figures

    def display_visualizations(self, screen):
        # Set up display parameters
        # make pygame screen larger to 1200
        screen = pygame.display.set_mode((1400, 1000))

        screen.fill((240, 240, 240))  # Light gray background
        
        # Calculate layout dimensions
        screen_width, screen_height = (1400, 1000)
        title_height = 40
        margin = 0
        graphs_area_height = screen_height - title_height - margin
        
        # 2x3 grid layout
        graph_width = (screen_width - 3 * margin) // 3
        graph_height = (graphs_area_height - 3 * margin) // 2
        
        # Add title first
        font = pygame.font.SysFont('Arial', 24)
        title = font.render('Game Performance Analytics', True, (0, 0, 0))
        screen.blit(title, (screen_width//2 - title.get_width()//2, 10))
        
        # Generate and display figures
        figures = self.generate_visualizations()
        
        for i, fig in enumerate(figures):
            # Set figure size to match our grid dimensions (convert pixels to inches)
            fig.set_size_inches(graph_width/100, graph_height/100)  # 100 DPI
            
            # Render figure
            fig.canvas.draw()
            buf = fig.canvas.buffer_rgba()
            size = fig.canvas.get_width_height()
            
            # Calculate position (2x3
            pos_x = (i % 3) * (graph_width + margin)
            pos_y = title_height + (i // 3) * (graph_height + margin)
            
            # Create surface and blit
            surf = pygame.image.frombuffer(buf, size, 'RGBA')
            screen.blit(surf, (pos_x, pos_y))
            plt.close(fig)
        
        pygame.display.flip()