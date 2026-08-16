import matplotlib.pyplot as plt


def plot_release_profiles(
    results,
    save_path="release_profiles.png"
):
    """
    Plot drug-release profiles for multiple
    nanoparticle sizes.
    """

    plt.figure(figsize=(10, 6))

    for result in results:

        plt.plot(
            result["time_hours"],
            result["release_percent"],
            linewidth=2,
            label=f'{result["radius_nm"]} nm'
        )

    plt.xlabel(
        "Time (hours)"
    )

    plt.ylabel(
        "Cumulative Drug Released (%)"
    )

    plt.title(
        "Predicted Drug Release from Nanoparticles"
    )

    plt.ylim(
        0,
        100
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend(
        title="Nanoparticle Radius"
    )

    plt.tight_layout()

    plt.savefig(
        save_path,
        dpi=300
    )

    plt.show()


def plot_sensitivity(
    radii,
    t50_values,
    t90_values,
    save_path="sensitivity_analysis.png"
):
    """
    Plot the effect of nanoparticle radius
    on t50 and t90.
    """

    fig, ax1 = plt.subplots(
        figsize=(10, 6)
    )

    ax1.plot(
        radii,
        t50_values,
        marker="o",
        label="t50"
    )

    ax1.set_xlabel(
        "Nanoparticle Radius (nm)"
    )

    ax1.set_ylabel(
        "t50 (hours)"
    )

    ax1.grid(
        True,
        alpha=0.3
    )

    ax2 = ax1.twinx()

    ax2.plot(
        radii,
        t90_values,
        marker="s",
        label="t90"
    )

    ax2.set_ylabel(
        "t90 (hours)"
    )

    plt.title(
        "Sensitivity of Drug Release to Nanoparticle Radius"
    )

    fig.tight_layout()

    plt.savefig(
        save_path,
        dpi=300
    )

    plt.show()