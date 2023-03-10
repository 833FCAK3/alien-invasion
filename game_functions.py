import sys
import pygame
import threading
import random
import math
import json
import time
from bullet import Bullet
from alien import Alien
from star import Star
from drop import Drop


def check_key_downs(event, ai_settings, screen, ship, bullets, stats, aliens):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_p:
        start_game(stats, aliens, bullets, ai_settings, screen, ship)
    if event.key == pygame.K_b:
        shield(ship, ai_settings)


def check_key_ups(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_key_downs(event, ai_settings, screen,
                            ship, bullets, stats, aliens)
        elif event.type == pygame.KEYUP:
            check_key_ups(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        start_game(stats, aliens, bullets, ai_settings, screen, ship)

        # Reset the scoreboard images.
        sb.prep_images()


def start_game(stats, aliens, bullets, ai_settings, screen, ship):
    """Start the game."""
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistics.
    stats.reset_stats()
    ai_settings.initialize_dynamic_settings()
    stats.game_active = True

    # Empty the list of aliens asnd bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, stars, drops,
                  ship, aliens, bullets, play_button, shield):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    stars.draw(screen)
    drops.draw(screen)
    shield.draw_shield(ai_settings, screen, ship)
    ship.blitme()
    aliens.draw(screen)
    ai_settings.end = time.time()
    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Respond to bullet-alien collision."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        start_new_level(ai_settings, bullets, stats, sb, screen, ship, aliens)


def start_new_level(ai_settings, bullets, stats, sb, screen, ship, aliens):
    """If the entire fleet is destroyed, start a new level."""
    bullets.empty()
    ai_settings.increase_speed()

    # Increase level.
    stats.level += 1
    sb.prep_level()

    create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in arow."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_stars_x(ai_settings, alien_width):
    """Determine the number of stars in a row."""
    star_number_x = int((ai_settings.screen_width - 0.5 *
                         alien_width) / alien_width)
    return star_number_x


def get_star_number_rows(ai_settings, alien_height):
    """Determine the number of star rows."""
    star_number_rows = int((ai_settings.screen_height - 0.5 *
                            alien_height) / alien_height)
    return star_number_rows


def create_star(ai_settings, screen, stars, aliens, star_number, star_row_number):
    """Create a star and place it in a row."""
    star = Star(ai_settings, screen)
    alien = Alien(ai_settings, screen)
    star.x = random.uniform(0.9, 1)*(0.5 * alien.rect.width +
                                     2 * alien.rect.width * star_number)
    star.rect.centerx = star.x
    star.rect.centery = random.uniform(0.9, 1)*((0.5 * alien.rect.height) +
                                                (2 * alien.rect.height * star_row_number))
    stars.add(star)


def create_star_grid(ai_settings, screen, stars, aliens):
    """Create a grid of stars."""
    star = Star(ai_settings, screen)
    alien = Alien(ai_settings, screen)
    star_number_x = get_star_number_rows(ai_settings, alien.rect.width)
    star_number_rows = get_star_number_rows(ai_settings, alien.rect.height)

    # Create the star grid.
    for row_number in range(star_number_rows):
        for star_number in range(star_number_x):
            create_star(ai_settings, screen, stars, aliens,
                        star_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if ship.shielded == 0:
        if stats.ships_left > 0:
            # Decrement ships_left.
            stats.ships_left -= 1

            # Update scoreboard.
            sb.prep_ships()

            # Empty the list of aliens and bullets.
            aliens.empty()
            bullets.empty()

            # Create a new fleet and center the ship.
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

            # Pause.
            time.sleep(0.5)

        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge,
     and then update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship.shielded = 0
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def create_drop(ai_settings, screen, drops):
    """Create a drop at a random place above the screen."""
    drop = Drop(ai_settings, screen)
    drop.x = random.randint(0, ai_settings.screen_width-100)
    drop.rect.x = drop.x
    drop.y = random.randint(-15, 15)
    drop.rect.y = drop.y
    drops.add(drop)


def create_rain(ai_settings, screen, drops):
    """Create a semblance of rain."""
    drop = Drop(ai_settings, screen)

    for instance_of_drop in range(15):
        create_drop(ai_settings, screen, drops)

    # for drop in drops.copy():
    #     if drop.rect.top >= 300:
    #         # for instance_of_drop in range(15):
    #         create_drop(ai_settings, screen, drops)


def update_drops(ai_settings, drops, screen):
    """Update positions of all the drops."""
    drops.update()

    # Remove drops that are off the screen.
    for drop in drops.copy():
        if drop.rect.top >= ai_settings.screen_height:
            drops.remove(drop)
            create_drop(ai_settings, screen, drops)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        write_new_high_score(stats)


def write_new_high_score(stats):
    """Write new high score to a file."""
    file_name = 'high_score.txt'
    with open(file_name, 'w') as file_object:
        json.dump(stats.high_score, file_object)
        # file_object.write(str(stats.high_score))


def shield(ship, ai_settings):
    """Ship becomes invincible for 3 seconds."""
    if ship.shield_available == 1:
        ship.shielded = 1
        ai_settings.start = time.time()

        # ship.shielded = 0
        # ship.shield_available = 0
