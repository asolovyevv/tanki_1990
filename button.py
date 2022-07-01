import pygame
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color=None):

		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.direct = 0
		self.timer = 60
		self.image_before = self.image

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if self.hovering_color != None:
			if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):

				self.text = self.font.render(self.text_input, True, self.hovering_color)
			else:
				self.text = self.font.render(self.text_input, True, self.base_color)
		else:
			pass

	def change_position(self, position, screen):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			if self.timer > 0:
				self.timer -= 1
			else:
				self.timer = 60
				self.image = pygame.transform.rotate(self.image, -90)
			screen.blit(self.image, self.rect)

		else:
			self.direct = 0
			self.image = self.image_before
			screen.blit(self.image, self.rect)
