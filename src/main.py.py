import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons

# Функция для создания начальных параметров
def create_initial_parameters():
    return {
        'lambda_': 500e-9,  # длина волны (м)
        'b': 0.1e-3,        # ширина щели (м)
        'd': 0.2e-3,        # расстояние между щелями (м)
        'N': 5,             # число щелей
        'L': 1.0            # расстояние до экрана (м)
    }

# Интенсивность для одиночной щели
def single_slit_intensity(x, params):
    theta = np.arctan(x / params['L'])
    beta = np.pi * params['b'] * np.sin(theta) / params['lambda_']
    beta = np.where(beta == 0, 1e-10, beta)
    return (np.sin(beta) / beta) ** 2

# Интенсивность для N щелей (общий случай)
def multi_slit_intensity(x, params):
    theta = np.arctan(x / params['L'])
    beta = np.pi * params['b'] * np.sin(theta) / params['lambda_']
    beta = np.where(beta == 0, 1e-10, beta)
    envelope = (np.sin(beta) / beta) ** 2
    alpha = np.pi * params['d'] * np.sin(theta) / params['lambda_']
    alpha = np.where(alpha == 0, 1e-10, alpha)
    N = int(params['N'])
    interference = (np.sin(N * alpha) / np.sin(alpha)) ** 2
    return envelope * interference

# Интенсивность для двойной щели (N=2)
def double_slit_intensity(x, params):
    p = params.copy()
    p['N'] = 2
    return multi_slit_intensity(x, p)

# Создание интерактивного графика
def create_plot():
    x = np.linspace(-0.01, 0.01, 2000)  # координаты экрана (м)
    params = create_initial_parameters()

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.3, bottom=0.4)

    # рассчитываем начальные интенсивности
    I1 = single_slit_intensity(x, params)
    I2 = double_slit_intensity(x, params)
    I3 = multi_slit_intensity(x, params)

    # рисуем кривые с объектами Line2D
    l_single, = ax.plot(x * 1e3, I1, label='Одна щель')
    l_double, = ax.plot(x * 1e3, I2, label='Двойная щель')
    l_multi, = ax.plot(x * 1e3, I3, label=f"{params['N']} щелей")

    # авто-масштаб по интенсивности
    def rescale():
        max_I = max(
            l.get_ydata().max() for l in (l_single, l_double, l_multi) if l.get_visible()
        ) if any(l.get_visible() for l in (l_single, l_double, l_multi)) else 1
        ax.set_ylim(0, max_I * 1.1)

    rescale()

    ax.set_xlabel('Координата на экране, x (мм)')
    ax.set_ylabel('Интенсивность')
    ax.set_title('ДИФРАКЦИЯ ФРАУНГОФЕРА СВЕТОВОГО ИЗЛУЧЕНИЯ')

    # Слайдеры параметров
    axcolor = 'lightgoldenrodyellow'
    ax_lambda = plt.axes([0.3, 0.25, 0.6, 0.03], facecolor=axcolor)
    ax_b      = plt.axes([0.3, 0.20, 0.6, 0.03], facecolor=axcolor)
    ax_d      = plt.axes([0.3, 0.15, 0.6, 0.03], facecolor=axcolor)
    ax_N      = plt.axes([0.3, 0.10, 0.6, 0.03], facecolor=axcolor)

    s_lambda = Slider(ax_lambda, 'Длина волны (нм)', 100, 1000, valinit=params['lambda_'] * 1e9)
    s_b      = Slider(ax_b, 'Толщина щели b (мкм)',     1,   500, valinit=params['b'] * 1e6)
    s_d      = Slider(ax_d, 'Расстояние между щелями d (мкм)',1,   1000,valinit=params['d'] * 1e6)
    s_N      = Slider(ax_N, 'Число щелей N',      1,   20,  valinit=params['N'], valstep=1)

    # Чекбоксы для вкл/выкл кривых
    ax_check = plt.axes([0.05, 0.4, 0.15, 0.15], facecolor=axcolor)
    check = CheckButtons(ax_check, ['Одна', 'Две', 'N щелей'], [True, True, True])

    def toggle(label):
        # переключаем видимость
        if label == 'Одна':
            l_single.set_visible(not l_single.get_visible())
        elif label == 'Две':
            l_double.set_visible(not l_double.get_visible())
        elif label == 'N щелей':
            l_multi.set_visible(not l_multi.get_visible())
        # обновляем легенду и масштаб
        ax.legend([l for l in (l_single, l_double, l_multi) if l.get_visible()],
                  [l.get_label() for l in (l_single, l_double, l_multi) if l.get_visible()])
        rescale()
        fig.canvas.draw_idle()

    check.on_clicked(toggle)

    # обновление при движении ползунков
    def update(val):
        params['lambda_'] = s_lambda.val * 1e-9
        params['b']       = s_b.val * 1e-6
        params['d']       = s_d.val * 1e-6
        params['N']       = int(s_N.val)

        I1 = single_slit_intensity(x, params)
        I2 = double_slit_intensity(x, params)
        I3 = multi_slit_intensity(x, params)

        l_single.set_ydata(I1)
        l_double.set_ydata(I2)
        l_multi.set_ydata(I3)
        # обновляем подпись для мульти
        l_multi.set_label(f"{params['N']} щелей")

        # обновляем легенду и масштаб
        ax.legend([l for l in (l_single, l_double, l_multi) if l.get_visible()],
                  [l.get_label() for l in (l_single, l_double, l_multi) if l.get_visible()])
        rescale()
        fig.canvas.draw_idle()

    # подписываем
    s_lambda.on_changed(update)
    s_b.on_changed(update)
    s_d.on_changed(update)
    s_N.on_changed(update)

    # финальная легенда
    ax.legend([l_single, l_double, l_multi], [l_single.get_label(), l_double.get_label(), l_multi.get_label()])
    plt.show()

if __name__ == '__main__':
    create_plot()  # запускаем визуализацию
