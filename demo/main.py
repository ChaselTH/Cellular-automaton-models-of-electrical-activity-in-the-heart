class Player:
    def __init__(self, health, ammo):
        self.health = health
        self.ammo = ammo

    def shoot(self, target):
        if self.ammo > 0:
            print("Bang!")
            target.health -= 1
            self.ammo -= 1
        else:
            print("Out of ammo.")


class Enemy:
    def __init__(self, health):
        self.health = health

    def attack(self, target):
        print("The enemy attacks!")
        target.health -= 1


player = Player(100, 10)
enemy = Enemy(3)

while player.health > 0 and enemy.health > 0:
    print(f"Player health: {player.health}. Ammo: {player.ammo}.")
    print(f"Enemy health: {enemy.health}.")
    player.shoot(enemy)
    if enemy.health > 0:
        enemy.attack(player)

if player.health > 0:
    print("You won!")
else:
    print("You lost.")
