from typing import Optional
import matplotlib.pyplot as plt

#   пример использования:
#   visualize([population_data], show=True, save=f'epoch_{i + 1}', title=f'Эпоха {i + 1}')
def visualize(
    input: list[list[int]], 
    show = True, 
    simultaneous = False,
    title: Optional[str] = None, 
    save: Optional[str] = None
):
    def __visualize_show(plt):
        if show:
            plt.show()
        
    def __visualize_title(fig):
        if title:
            fig.suptitle(title, fontsize=20)

    def __visualize_save(plt):
        if (save):
            plt.savefig(f'./result/{save}.png')

    def __visualize_one(input: list[int]):
        fig = plt.figure()
        __visualize_title(fig)
        plt.plot(input)
        plt.ylim(ymin=0)

        __visualize_save(plt)
        __visualize_show(plt)
        plt.close('all')

    def __visualize_many_simultaneous(input: list[list[int]]):
        fig = plt.figure()
        __visualize_title(fig)
        for data in input:
            plt.plot(data)
        plt.ylim(ymin=0)
        
        __visualize_save(plt)
        __visualize_show(plt)
        plt.close('all')

    def __visualize_many(input: list[list[int]]):
        fig, axs = plt.subplots(count)
        __visualize_title(fig)
        for index, data in enumerate(input):
            axs[index].plot(data)

        __visualize_save(plt)
        __visualize_show(plt)
        plt.close('all')

    count = len(input)
    if (count == 1):
        __visualize_one(input[0])
    else:
        if (simultaneous):
            __visualize_many_simultaneous(input)
        else :
            __visualize_many(input)
