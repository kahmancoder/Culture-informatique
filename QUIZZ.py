import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Culture Informatique")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)
LIGHT_BLUE = (100, 180, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)

# Police
font_large = pygame.font.SysFont("Arial", 36)
font_medium = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 22)

# Questions et réponses
questions = [
    {
        "question": "Qui est considéré comme le premier programmeur de l'histoire?",
        "options": ["Alan Turing", "Ada Lovelace", "Bill Gates", "Charles Babbage"],
        "answer": 1
    },
    {
        "question": "Quel langage a été créé par Guido van Rossum?",
        "options": ["Java", "Python", "C++", "JavaScript"],
        "answer": 1
    },
    {
        "question": "Quelle société a développé le microprocesseur Intel 8086?",
        "options": ["AMD", "Intel", "IBM", "Motorola"],
        "answer": 1
    },
    {
        "question": "En quelle année a été créé le World Wide Web?",
        "options": ["1989", "1995", "2000", "1975"],
        "answer": 0
    },
    {
        "question": "Quel est le nom du premier ordinateur électronique?",
        "options": ["ENIAC", "UNIVAC", "IBM 701", "Z3"],
        "answer": 0
    },
    {
        "question": "Quel protocole est utilisé pour transférer des pages web?",
        "options": ["FTP", "HTTP", "SMTP", "TCP"],
        "answer": 1
    },
    {
        "question": "Quel langage est principalement utilisé pour le développement web frontend?",
        "options": ["Python", "Java", "JavaScript", "C#"],
        "answer": 2
    },
    {
        "question": "Qu'est-ce qu'un 'bug' en informatique?",
        "options": ["Un virus", "Une erreur dans un programme", "Un composant matériel", "Un type de firewall"],
        "answer": 1
    },
    {
        "question": "Quel système d'exploitation a été créé par Linus Torvalds?",
        "options": ["Windows", "macOS", "Linux", "Unix"],
        "answer": 2
    },
    {
        "question": "Que signifie l'acronyme 'HTML'?",
        "options": ["HyperText Markup Language", "HighTech Modern Language", 
                   "HyperTransfer Markup Language", "HighLevel Text Model"],
        "answer": 0
    }
]

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = LIGHT_BLUE
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font_medium.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Game:
    def __init__(self):
        self.questions = questions.copy()
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.answered = False
        self.game_over = False
        
        # Créer les boutons de réponse
        self.option_buttons = []
        for i in range(4):
            button = Button(150, 300 + i*70, 500, 50, "", BLUE)
            self.option_buttons.append(button)
            
        self.next_button = Button(350, 500, 100, 50, "Suivant", GREEN)
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.game_over:
                if self.next_button.is_clicked(mouse_pos, event):
                    self.__init__()  # Redémarrer le jeu
                continue
                
            if self.answered:
                if self.next_button.is_clicked(mouse_pos, event):
                    self.next_question()
                continue
                
            for i, button in enumerate(self.option_buttons):
                if button.is_clicked(mouse_pos, event):
                    self.check_answer(i)
                    
        # Mettre à jour l'état de survol des boutons
        for button in self.option_buttons:
            button.check_hover(mouse_pos)
        self.next_button.check_hover(mouse_pos)
        
    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.game_over = True
        else:
            self.answered = False
            
    def check_answer(self, selected_option):
        correct_answer = self.questions[self.current_question]["answer"]
        self.answered = True
        
        if selected_option == correct_answer:
            self.score += 1
            
    def draw(self):
        screen.fill(WHITE)
        
        if self.game_over:
            # Afficher le score final
            title = font_large.render("Quiz Terminé!", True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            score_text = font_medium.render(f"Votre score: {self.score}/{len(self.questions)}", True, BLACK)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
            
            self.next_button.text = "Rejouer"
            self.next_button.draw(screen)
            return
            
        # Afficher la question
        question_text = self.questions[self.current_question]["question"]
        question_surface = font_medium.render(question_text, True, BLACK)
        screen.blit(question_surface, (WIDTH//2 - question_surface.get_width()//2, 100))
        
        # Afficher le score actuel
        score_text = font_small.render(f"Score: {self.score}/{self.current_question}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        # Afficher le numéro de la question
        question_num = font_small.render(f"Question {self.current_question + 1}/{len(self.questions)}", True, BLACK)
        screen.blit(question_num, (WIDTH - question_num.get_width() - 20, 20))
        
        # Afficher les options de réponse
        options = self.questions[self.current_question]["options"]
        correct_answer = self.questions[self.current_question]["answer"]
        
        for i, button in enumerate(self.option_buttons):
            button.text = options[i]
            
            if self.answered:
                if i == correct_answer:
                    button.color = GREEN
                elif button.color != GREEN:  # Ne pas changer la couleur si c'est déjà vert
                    button.color = GRAY
            else:
                button.color = BLUE
                
            button.draw(screen)
            
        if self.answered:
            self.next_button.draw(screen)

# Boucle principale du jeu
def main():
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        game.handle_events()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()