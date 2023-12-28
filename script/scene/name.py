from pygame_textinput import *

from script.scene import *
from script.text import TextRender
from script.state import state
from script.data import check_data, save_data


class Name(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.render = TextRender(screen, size=24, color=(24, 24, 30))
        manager = TextInputManager(validator=lambda i: len(i) <= 12)
        font = pygame.font.Font("resource/font/Jalnan2TTF.ttf", size=42)
        self.textinput = TextInputVisualizer(manager=manager, font_object=font)

        self.place = check_data(state.game, state.score)

    def get_event(self) -> Optional[callback]:
        from script.scene.title import Title
        from script.scene.result import Result

        events = pygame.event.get()
        self.textinput.update(events)
        self.textinput.value = self.textinput.value.lstrip()
        for event in events:
            if event.type == pygame.QUIT:
                return End
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return Title
            if event.key == pygame.K_RETURN:
                if self.textinput.value.strip() == "":
                    continue
                save_data(state.game, self.textinput.value, state.score)
                return Result

    def run(self) -> Optional[callback]:
        from script.scene.result import Result

        result = self.get_event()
        if result is not None:
            return result

        if self.place >= 10:
            return Result

        self.render("이름을 입력해주세요!", (960, 360), size=64)
        self.render(f"순위: {self.place + 1}등", (960, 420))
        self.screen.blit(self.textinput.surface, self.textinput.surface.get_rect(center=(960, 540)))
        self.render("한글은 입력이 불가능합니다...", (960, 660))
        self.render("만약 입력이 안 되는 경우 한영키를 눌러주세요", (960, 700))
