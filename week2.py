import random
import time


TOTAL_CYCLE = 90  


def get_traffic_jam_score(ns_green):
    ew_green = TOTAL_CYCLE - ns_green

    if ns_green < 10 or ew_green < 10:
        return 999

    ns_delay = 45 * ((TOTAL_CYCLE - ns_green) / 60)
    ew_delay = 15 * ((TOTAL_CYCLE - ew_green) / 60)

    return round(ns_delay + ew_delay, 1)


bird_positions = [20.0, 50.0, 85.0]  
bird_speeds = [2.0, -3.0, 1.0]  

bird_pbest_pos = list(bird_positions)
bird_pbest_score = [get_traffic_jam_score(p) for p in bird_positions]

gbest_index = bird_pbest_score.index(min(bird_pbest_score))
gbest_pos = bird_pbest_pos[gbest_index]

print("--- STARTING THE SWARM SIMULATION ---")
print(f"Initial Bird Guesses: Bird 1={bird_positions[0]}s, Bird 2={bird_positions[1]}s, Bird 3={bird_positions[2]}s")
print(f"Flock's Initial Best Idea: {gbest_pos} seconds (Score: {bird_pbest_score[gbest_index]} stuck cars)\n")

MAX_ITERATIONS = 4
w, c1, c2 = 0.5, 1.5, 1.5  

for iteration in range(1, MAX_ITERATIONS + 1):
    print(f"=== ITERATION {iteration} ===")

    for i in range(3):
  
        r1, r2 = random.random(), random.random()

    
        personal_pull = c1 * r1 * (bird_pbest_pos[i] - bird_positions[i])
        flock_pull = c2 * r2 * (gbest_pos - bird_positions[i])
        bird_speeds[i] = (w * bird_speeds[i]) + personal_pull + flock_pull


        bird_positions[i] = round(bird_positions[i] + bird_speeds[i], 1)

        bird_positions[i] = max(10.0, min(80.0, bird_positions[i]))


        current_score = get_traffic_jam_score(bird_positions[i])

        print(
            f"  Bird {i+1} flies to {bird_positions[i]}s green light -> Traffic Jam Score: {current_score} cars"
        )


        if current_score < bird_pbest_score[i]:
            bird_pbest_score[i] = current_score
            bird_pbest_pos[i] = bird_positions[i]
            print(f"    Bird {i+1} found a better personal configuration!")


    gbest_index = bird_pbest_score.index(min(bird_pbest_score))
    gbest_pos = bird_pbest_pos[gbest_index]

    print(
        f"End of Iteration {iteration}: The current winning schedule is {gbest_pos}s of green light.\n"
    )
    time.sleep(0.5)  


print("--- FINAL OPTIMIZED TIMING REACHED ---")
print(f"Optimal North-South Green Light: {round(gbest_pos)} seconds")
print(f"Optimal East-West Green Light: {round(TOTAL_CYCLE - gbest_pos)} seconds")
print(f"Final Minimised Traffic Jam Score: {min(bird_pbest_score)} stuck cars")
