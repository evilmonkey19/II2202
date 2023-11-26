import os
import time
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse
import numpy as np

def get_difference_timings_sender_receiver(index: int, type: str, server: bool = False):
    sender_timings: dict[int, datetime] = dict()
    filename: str = f"{type}/clients/{index}/sender_timings.csv"
    if server:
        filename = f"{type}/servers/server_{index}.csv"
    with open(filename, "r") as sender_file:
        sender_lines = sender_file.readlines()
        for line in sender_lines:
            hash_value = int(line.split(",")[0])
            timing = parse(line.split(",")[1])
            sender_timings[hash_value] = timing
    
    all_receiver_timings: list[dict[int, datetime]] = list()
    for i in range(index):
        receiver_timings: dict[int, datetime] = dict()
        with open(f"{type}/clients/{index}/client_recv_{i}.csv", "r") as receiver_file:
            receiver_lines = receiver_file.readlines()
            for line in receiver_lines:
                hash_value = int(line.split(",")[0])
                timing = parse(line.split(",")[1])
                receiver_timings[hash_value] = timing
        all_receiver_timings.append(receiver_timings)

    diff_sender_receiver: list[list[int]] = list()
    for hash_value, timing in sender_timings.items():
        diff_timings: list[int] = list()
        for receiver_timing in all_receiver_timings:
            diff_timings.append(max(0, (receiver_timing[hash_value] - timing).total_seconds()))
        diff_sender_receiver.append(diff_timings)

    avg_diff_timings: list[int] = list()
    for timings in diff_sender_receiver:
        avg_diff_timings.append(sum(timings) / len(timings))
    return avg_diff_timings

if __name__ == "__main__":
    graphql_diff_sender_receiver: list[list[int]] = []
    for i in range(1, 11):
        graphql_diff_sender_receiver.append(get_difference_timings_sender_receiver(i, 'graphql'))
    websockets_diff_sender_receiver: list[list[int]] = []
    for i in range(1, 11):
        websockets_diff_sender_receiver.append(get_difference_timings_sender_receiver(i, 'websockets'))
    
    # Plotting the average of each experiment
    experiment_numbers = list(range(1, 11))

    # Calculate averages
    average_times_graphql = [sum(diff) / len(diff) for diff in graphql_diff_sender_receiver]
    average_times_websockets = [sum(diff) / len(diff) for diff in websockets_diff_sender_receiver]

    # Plot GraphQL averages
    plt.plot(experiment_numbers, average_times_graphql, label='GraphQL')

    # Plot Websockets averages
    plt.plot(experiment_numbers, average_times_websockets, label='Websockets')

    # Add labels and title
    plt.xlabel('Number of Receivers')
    plt.ylabel('Average Time')
    plt.title('Average Time from Sender to Receiver')

    # Add legend
    plt.legend()

    # Show the plot
    # plt.show()

    plt.savefig('../docs/pictures/average_time_sender_receiver.svg', format='svg')
    plt.savefig('../docs/pictures/average_time_sender_receiver.jpeg', format='jpeg')

    plt.clf()


    # Plotting the standard deviation of each experiment
    experiment_numbers = list(range(1, 11))
    standard_deviations_grapql = [np.std(diff) for diff in graphql_diff_sender_receiver]
    standard_deviations_websockets = [np.std(diff) for diff in websockets_diff_sender_receiver]
    plt.plot(experiment_numbers, standard_deviations_grapql, label='GraphQL')
    plt.plot(experiment_numbers, standard_deviations_websockets, label='Websockets')
    plt.xlabel('Number of Receivers')
    plt.ylabel('Standard Deviation')
    plt.title('Standard Deviation from Sender to Receiver')
    plt.legend()
    # plt.show()

    plt.savefig('../docs/pictures/standard_deviation_time_sender_receiver.svg', format='svg')
    plt.savefig('../docs/pictures/standard_deviation_time_sender_receiver.jpeg', format='jpeg')

    plt.clf()
    

    graphql_diff_server_receiver: list[list[int]] = []
    for i in range(1, 11):
        graphql_diff_server_receiver.append(get_difference_timings_sender_receiver(i, 'graphql', server=True))
    websockets_diff_server_receiver: list[list[int]] = []
    for i in range(1, 11):
        websockets_diff_server_receiver.append(get_difference_timings_sender_receiver(i, 'websockets', server=True))

    # Plotting the average of each experiment
    experiment_numbers = list(range(1, 11))

    # Calculate averages
    average_times_graphql = [sum(diff) / len(diff) for diff in graphql_diff_server_receiver]
    average_times_websockets = [sum(diff) / len(diff) for diff in websockets_diff_server_receiver]

    # Plot GraphQL averages
    plt.plot(experiment_numbers, average_times_graphql, label='GraphQL')

    # Plot Websockets averages
    plt.plot(experiment_numbers, average_times_websockets, label='Websockets')

    # Add labels and title
    plt.xlabel('Number of Receivers')
    plt.ylabel('Average Time')
    plt.title('Average Time from Server to Receiver')

    # Add legend
    plt.legend()

    # Show the plot
    # plt.show()

    plt.savefig('../docs/pictures/average_time_server_receiver.svg', format='svg')
    plt.savefig('../docs/pictures/average_time_server_receiver.jpeg', format='jpeg')

    plt.clf()

    # Plotting the standard deviation of each experiment
    experiment_numbers = list(range(1, 11))
    standard_deviations_grapql = [np.std(diff) for diff in graphql_diff_server_receiver]
    standard_deviations_websockets = [np.std(diff) for diff in websockets_diff_server_receiver]
    plt.plot(experiment_numbers, standard_deviations_grapql, label='GraphQL')
    plt.plot(experiment_numbers, standard_deviations_websockets, label='Websockets')
    plt.xlabel('Number of Receivers')
    plt.ylabel('Standard Deviation')
    plt.title('Standard Deviation from Server to Receiver')
    plt.legend()
    # plt.show()

    plt.savefig('../docs/pictures/standard_deviation_time_server_receiver.svg', format='svg')
    plt.savefig('../docs/pictures/standard_deviation_time_server_receiver.jpeg', format='jpeg')

    plt.clf()
