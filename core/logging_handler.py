import logging

logging.basicConfig(
    filename='coder.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_analysis(issues):
    logging.info(f"Результаты анализа: {issues}")

def log_fix(fixed_code):
    logging.info(f"Исправленный код:\n{fixed_code}")

def log_improvements(improved_code):
    logging.info(f"Улучшенный код:\n{improved_code}")