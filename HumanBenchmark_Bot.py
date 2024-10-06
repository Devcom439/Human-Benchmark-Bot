import time
import selenium
import keyboard as kb
from selenium import webdriver
import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Chrome driver options
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# URLs of the tests on the Human Benchmark website
test_urls = {
    "reaction time": "https://humanbenchmark.com/tests/reactiontime",
    "aim trainer": "https://humanbenchmark.com/tests/aim",
    "chimp test": "https://humanbenchmark.com/tests/chimp",
    "typing": "https://humanbenchmark.com/tests/typing",
    "sequence memory": "https://humanbenchmark.com/tests/sequence",
    "number memory": "https://humanbenchmark.com/tests/number-memory",
    "verbal memory": "https://humanbenchmark.com/tests/verbal-memory",
    "visual memory": "https://humanbenchmark.com/tests/memory",
}

def consent(driver: webdriver.Chrome) -> None:
    """
    Clicks the consent button if it appears on the page.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
    
    Returns:
        None
    """
    try:
        consent_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class='fc-button fc-cta-consent fc-primary-button']"))
        )
        consent_button.click()
    except Exception:
        print("Error consenting")

def press_start_continue_btn(driver: webdriver.Chrome) -> None:
    """
    Clicks the start or continue button to begin a test.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
    
    Returns:
        None
    """
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr e19owgy710')]"))
    ).click()

def remove_ad(driver: webdriver.Chrome, timeout: int = 2) -> None:
    """
    Removes any blocking ad by clicking the ad if it appears.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        timeout (int, optional): The time to wait for the ad to appear. Defaults to 2 seconds.
    
    Returns:
        None
    """
    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located(
            (By.XPATH, "//div[starts-with(@style, 'grid-column: 4 / 4; place-self: center right; cursor: pointer;')]"))).click()
        print("Removed blocking ad")
    except Exception:
        pass

def get_current_level(driver: webdriver.Chrome) -> int:
    """
    Retrieves the current level number during a memory test.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
    
    Returns:
        int: The current level number or None if the level could not be retrieved.
    """
    try:
        level_element = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, "//span[@class='css-dd6wi1']//span[2]"))
        )
        level_number = int(level_element.text)
        print(f"Current level: {level_number}")
        return level_number
    except selenium.common.exceptions.TimeoutException:
        print("Failed to retrieve the current level.")
        return None

def reaction_time(driver: webdriver.Chrome, tries: int = 1) -> None:
    """
    Runs the Reaction Time test for a specified number of attempts and prints the best reaction time.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        tries (int, optional): Number of reaction time attempts. Defaults to 1.
    
    Returns:
        None
    """
    reaction_div_start = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'view-splash')]"))
    )
    reaction_div_start.click()

    best_time = float('inf')

    for attempt in range(tries):
        reaction_div_stop = WebDriverWait(driver, 20, poll_frequency=0.1).until(
            ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'view-go')]"))
        )
        reaction_div_stop.click()

        result_div = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, "//div[@class='css-1qvtbrk e19owgy78']/h1"))
        )
        reaction_time_result = result_div.text
        print(f"Reaction time for attempt {attempt + 1}: {reaction_time_result}")

        reaction_time_float = float(reaction_time_result.strip('ms'))
        if reaction_time_float < best_time:
            best_time = reaction_time_float

        if attempt + 1 < tries:
            continue_button = WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((By.CLASS_NAME, "view-result"))
            )
            continue_button.click()

    print(f"Best reaction time after {tries} tries: {int(best_time)} ms")

def aim(driver: webdriver.Chrome) -> None:
    """
    Runs the Aim Trainer test by clicking 30 targets as quickly as possible.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
    
    Returns:
        None
    """
    for _ in range(31):
        target = WebDriverWait(driver, 2, poll_frequency=0.1).until(
            ec.element_to_be_clickable((By.XPATH, "//div[starts-with(@class, 'css-17nnhwz') and starts-with(@style, 'width: 100px')]"))
        )
        target.click()

    score = WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'css-0')]"))
    ).text
    print(f"Average time per target: {score}")

def chimp(driver: webdriver.Chrome) -> None:
    """
    Runs the Chimp Test by clicking numbers in the correct order.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
    
    Returns:
        None
    """
    press_start_continue_btn(driver)

    while True:
        blocks = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.XPATH, "//div[@data-cellnumber]"))
        )
        
        blocks_with_numbers = [(block, int(block.get_attribute("data-cellnumber"))) for block in blocks]
        blocks_with_numbers.sort(key=lambda x: x[1])
        
        for block, _ in blocks_with_numbers:
            block.click()

        try:
            press_start_continue_btn(driver)
        except selenium.common.exceptions.TimeoutException:
            break

def typing(driver: webdriver.Chrome, realism: bool) -> None:
    """
    Runs the Typing test with either realistic or unrealistic typing speed.
    
    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        realism (bool): If True, simulate realistic typing speed; otherwise, type the text instantly.
    
    Returns:
        None
    """
    typing_window = WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'letters notranslate')]"))
    )

    remaining_letters = WebDriverWait(driver, 5).until(
        ec.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'incomplete')]"))
    )

    if realism:
        text_to_type = ''.join([letter.text if letter.text != '' else ' ' for letter in remaining_letters])
        chunk_size = 5
        for i in range(0, len(text_to_type), chunk_size):
            chunk = text_to_type[i:i + chunk_size]
            typing_window.send_keys(chunk)
            time.sleep(0.1)
    else:
        text_to_type = ''.join([letter.text if letter.text else ' ' for letter in remaining_letters])
        typing_window.send_keys(text_to_type)

    wmp = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'css-0')]"))
    ).text
    print(f"Words typed per minute: {wmp}")

def sequence(driver: webdriver.Chrome, stop_key: str) -> None:
    """
    Runs the sequence memory test until the stop_key is pressed.

    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        stop_key (str): The key to stop the test which goes on indefinitely
        
    Returns:
        None
    """
    # Start the sequence memory test by clicking the start button
    press_start_continue_btn(driver)

    # Initialize an empty list to store the full sequence
    sequence_list: list = []
    squares_wrong: int = 0

    while not kb.is_pressed(stop_key):
        try:
            # Capture the new squares in the sequence
            new_squares: list = []
            level_number: int = get_current_level(driver)  # Get the current level

            while True:
                try:
                    # Wait for an active square to appear
                    active_square = WebDriverWait(driver, 10, poll_frequency=0.05).until(
                        ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'square active')]"))
                    )

                    # Add the WebElement only if it hasn't been captured before
                    new_squares.append(active_square)

                    # Break the loop if no new squares appear for 0.5 seconds (end of sequence for the level)
                    try:
                        WebDriverWait(driver, 0.5).until(
                            ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'square active')]"))
                        )
                    except selenium.common.exceptions.TimeoutException:
                        # No more squares, end of current level sequence
                        print("New sequence captured.")
                        break

                except selenium.common.exceptions.TimeoutException:
                    # If no active square appears, assume sequence capturing is over
                    print("No more squares activated.")
                    break

            # Ensure the sequence list contains the correct number of squares (matching the level number)
            while len(sequence_list) < level_number and new_squares:
                sequence_list.append(new_squares[-1])  # Add the last square in case of duplicates

            # Click all squares in the correct sequence order
            print("Clicking captured squares in order.")
            for idx in range(len(sequence_list)):
                try:
                    # Re-locate the current square before clicking to avoid stale references
                    square = sequence_list[idx]
                    # Confirm the square is still displayed and active
                    if square.is_displayed():
                        print(f"Clicking square {idx + 1}")
                        square.click()
                    else:
                        print(f"Square {idx + 1} is not displayed, skipping.")

                # If the bot captured a wrong square, the game will end. If a stale element is found three times, the game definitely ended
                except selenium.common.exceptions.StaleElementReferenceException:
                    print(f"Stale element encountered for square {idx + 1}, skipping.")
                    squares_wrong += 1

                    if squares_wrong >= 3:
                        print("Bot clicked wrong square. Game ended")
                        break
                    continue

            # Wait for the next level to start (indicated by new square activation)
            print("Waiting for the next level...")

        except IndexError:
            print("Failed to capture a square")
            break

        except selenium.common.exceptions.TimeoutException:
            print("Sequence Memory test completed or failed.")
            break

    else:
        print("Key pressed, stopping test...")
        driver.quit()

def number(driver: webdriver.Chrome) -> None:
    """
    Runs the number memory test until the test is completed.

    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        
    Returns:
        None
    """
    # Start the test by pressing the start/continue button
    press_start_continue_btn(driver)

    while True:
        try:
            number_elem = WebDriverWait(driver, 30).until(
                ec.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'big-number ')]")
                )
            )
            number = number_elem.text
            print(f"Captured number: {number}")

            input_elem = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//form//div[@class='css-1qvtbrk e19owgy78']/input[@type='text']")))

            input_elem.send_keys(number)

            # Press the submit button
            press_start_continue_btn(driver)
            # Press the continue button
            press_start_continue_btn(driver)

        except selenium.common.exceptions.TimeoutException:
            break

def verbal(driver: webdriver.Chrome, stop_key) -> None:
    """
    Runs the verbal memory test until the stop_key is pressed.

    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        stop_key (_type_): The key to stop the test which goes on indefinitely
        
    Returns: None
    """
    press_start_continue_btn(driver)  # Start the test
    seen_words = []  # List to track the seen words
    lives = 3        # Start with 3 lives (as indicated in the UI)
    score = 0        # Start score

    while not kb.is_pressed(stop_key):
        while lives > 0 and not kb.is_pressed(stop_key):
            try:
                # Capture the current word displayed
                word_elem = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'word')]"))
                )
                word = word_elem.text
                print(f"Captured word: {word}")

                # Check if the word has been seen before
                if word in seen_words:
                    print(f"{word} is seen already")

                    # Click the "SEEN" button
                    seen_btn = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.XPATH, "//button[text()='SEEN']"))
                    )
                    seen_btn.click()
                else:
                    print(f"{word} is a new word")
                    # Add new word to seen words list
                    seen_words.append(word)

                    # Click the "NEW" button
                    new_btn = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.XPATH, "//button[text()='NEW']"))
                    )
                    new_btn.click()

                # Capture updated score and lives after the action
                score = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//span[contains(@class, 'score')]"))
                ).text

                lives = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//span[contains(@class, 'lives')]"))
                ).text

                print(f"Score: {score}, Lives: {lives}")
                
                lives = int(lives.lstrip("Lives | "))

            except selenium.common.exceptions.TimeoutException:
                print("Game stopped")
                break

    print(f"Final Score: {score}")

def visual(driver: webdriver.Chrome, stop_key) -> None:
    """
    Runs the visual memory test until the stop_key is pressed.

    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        stop_key (_type_): The key to stop the test which goes on indefinitely.
        
    Returns: None
    """
    press_start_continue_btn(driver)
    
    while not kb.is_pressed(stop_key):
        try:
            try:
                active_squares = WebDriverWait(driver, 1, poll_frequency=0.1).until(ec.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'active css-lxtdud eut2yre1')]")))
            except selenium.common.exceptions.TimeoutException:
                for square in active_squares:
                    square.click()
                
                get_current_level()
            
        except selenium.common.exceptions.TimeoutException:
            print("Game stopped")
            break
        except selenium.common.exceptions.StaleElementReferenceException:
            break
        
    else:
        print("Key pressed, stopping test...")
        driver.quit()
    
def all(driver: webdriver.Chrome, tries, stop_key) -> None:
    """
    Runs all tests

    Args:
        driver (webdriver.Chrome): The web driver instance for controlling the browser.
        tries (_type_): _description_
        stop_key (_type_): The key to stop the test which goes on indefinitely
        
    Returns: None
    """
    reaction_time(driver, tries)
    aim(driver)
    chimp(driver)
    typing(driver)
    sequence(driver, stop_key)
    number(driver)
    verbal(driver)
    visual(driver)

def main():
    # Prompt user for test selection
    while True:
        test = input('''Which mode? Choose from:
-Reaction time
-Aim Trainer
-Chimp Test
-Typing
-Sequence Memory
-Number Memory
-Verbal Memory
-Visual Memory
-All of them
Choice: ''').lower()

        # Check if the input is valid
        if 'all' in test:
                break
        if test not in test_urls:
            print("\nInvalid choice, please try again.")
            continue
        break
    
    tries = None
    stop_key = None
    if test in ['all of them', 'reaction time']:
        tries = int(input("Amount of tries (multiple reccomended): "))

    if test in ['all of them', 'verbal memory', 'sequence memory', 'visual memory']:
        while True:
            stop_key = input("Key to stop the sequence and verbal bot (they go on indefinitely): ")

            if len(stop_key) > 1:
                print("The stop key can only contain 1 character")
                continue
            break
        
    if test in ['all of them', 'typing']:
        realism = True
        
        while True:
            realism_input = input("Realism of the typing (realistic or unrealistic): ").lower().strip()
            
            if realism_input == 'realistic':
                realism = True
                break
            elif realism_input == 'unrealistic':
                realism = False
                break
            else:
                print("Invalid realism option, please choose realistic or unrealistic.")
                continue
    # Mapping test to its respective function
    test_functions = {
        'reaction time': lambda: reaction_time(driver, tries),
        'aim trainer': lambda: aim(driver),
        'chimp test': lambda: chimp(driver),
        'typing': lambda: typing(driver, realism),
        'sequence memory': lambda: sequence(driver, stop_key),
        'number memory': lambda: number(driver),
        'verbal memory': lambda: verbal(driver, stop_key),
        'visual memory': lambda: visual(driver, stop_key),
    }

    # Run all tests if "all" was selected
    if 'all' in test:
        for test_name, test_function in test_functions.items():
            print(f"Running {test_name.replace('_', ' ').title()}")

            driver = webdriver.Chrome(options=options)
            driver.get(test_urls[test_name])

            consent(driver)
            remove_ad(driver, 10)
            test_function()

    # Run a single selected test
    else:
        driver = webdriver.Chrome(options=options)
        driver.get(test_urls[test])

        consent(driver)
        remove_ad(driver, 10)
        test_functions[test]()

if __name__ == "__main__":
    try:
        main()
    except selenium.common.exceptions.NoSuchWindowException:
        pass
