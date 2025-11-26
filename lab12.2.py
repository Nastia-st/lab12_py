import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool

def load_data():
    #Завантаження CSV з обробкою помилок
    while True:
        file_path = input("Введіть шлях до CSV файлу: ")
        try:
            df = pd.read_csv(file_path, delimiter=',', on_bad_lines='skip', engine='python')
            print("Файл успішно завантажено.")
            return df
        except FileNotFoundError:
            print("Помилка: файл не знайдено. Спробуйте ще раз.")
        except Exception as e:
            print(f"Помилка читання файлу: {e}")
def clean_data(df):
    #Очищення даних та визначення числових колонок
    clean_df = df.dropna()
    numeric_cols = clean_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if not numeric_cols:
        raise ValueError("У файлі немає числових колонок!")
    return clean_df, numeric_cols
def build_plot(clean_df, column):
    #Побудова інтерактивного графіка Bokeh
    x = list(range(len(clean_df)))
    y = clean_df[column].values
    plot = figure(title=f"Інтерактивний графік для колонки: {column}",
                  x_axis_label="Індекс",
                  y_axis_label=column,
                  tools="pan,wheel_zoom,box_zoom,reset,hover")
    plot.line(x, y, line_width=2)
    hover = plot.select_one(HoverTool)
    hover.tooltips = [("Індекс", "@x"), (column, "@y")]
    return plot

def save_results(clean_df, plot):
    #Збереження результатів
    clean_df.to_csv("cleaned_data.csv", index=False)
    output_file("interactive_plot.html")
    save(plot)
    print("Результати збережено у файли cleaned_data.csv та interactive_plot.html")
def main():
    df = load_data()
    clean_df, numeric_cols = clean_data(df)
    print("\nДоступні числові колонки:")
    for col in numeric_cols:
        print("-", col)
    column = input("Введіть назву колонки для візуалізації: ")
    while column not in numeric_cols:
        print("Помилка: такої колонки немає серед числових. Спробуйте ще раз.")
        column = input("Введіть назву колонки: ")
    plot = build_plot(clean_df, column)
    save_results(clean_df, plot)
    print("Готово. Відкрийте interactive_plot.html для перегляду графіка.")
main()