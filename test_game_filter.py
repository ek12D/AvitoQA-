import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL тестируемого приложения
URL = "https://makarovartem.github.io/frontend-avito-tech-test-assignment/"

@pytest.fixture(scope="module")
def driver():
    # Инициализация веб-драйвера
    driver = webdriver.Chrome()  # Убедитесь, что ChromeDriver установлен и доступен в PATH
    driver.get(URL)
    yield driver
    driver.quit()

def test_filter_by_genre(driver):
    # Фильтрация по жанру
    genre_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='Filter by category']"))
    )
    genre_dropdown.click()
    genre_option = driver.find_element(By.XPATH, "//option[text()='mmorpg']")
    genre_option.click()
    
    apply_filter_button = driver.find_element(By.XPATH, "//button[text()='Apply filter']")
    apply_filter_button.click()
    
    time.sleep(2)  # Ожидание обновления страницы
    
    # Проверка, что отображаются только игры жанра "mmorpg"
    games = driver.find_elements(By.CLASS_NAME, "game-card")
    for game in games:
        assert "mmorpg" in game.text, "Game genre does not match the filter"

def test_return_to_main_page(driver):
    # Переход на страницу карточки игры
    first_game = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='game-card'][1]"))
    )
    first_game.click()
    
    # Нажатие кнопки "Back to main"
    back_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Back to main']"))
    )
    back_button.click()
    
    time.sleep(2)  # Ожидание обновления страницы
    
    # Проверка, что пользователь вернулся на главную страницу
    assert "Game Collection" in driver.title, "Did not return to main page"

def test_pagination(driver):
    # Выполнение поиска, чтобы получить несколько страниц результатов
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='search']"))
    )
    search_input.send_keys("Game")
    
    search_button = driver.find_element(By.XPATH, "//button[text()='Search']")
    search_button.click()
    
    time.sleep(2)  # Ожидание обновления страницы
    
    # Переход на следующую страницу
    next_page_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    next_page_button.click()
    
    time.sleep(2)  # Ожидание обновления страницы
    
    # Проверка, что отображаются результаты на следующей странице
    assert "Page 2" in driver.page_source, "Did not navigate to the next page"

    # Переход на предыдущую страницу
    prev_page_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Previous']"))
    )
    prev_page_button.click()
    
    time.sleep(2)  # Ожидание обновления страницы
    
    # Проверка, что отображаются результаты на предыдущей странице
    assert "Page 1" in driver.page_source, "Did not navigate back to the previous page"
