import random
import statistics
import numpy as np

num_trials      = 10000
prehammer       = True
slots           = 7
success_prob    = 0.39
roll_cost       = 1350
css_cost        = 20000
ark_cost        = 24000
hammer_cost     = 24000

def calculate(base_slots, prehammer):
    if prehammer:
        print(f"You intend to hammer a item with {base_slots} slots before scrolling")    
    else:
        print(f"You intend to hammer a item with {base_slots} after a thresold")

    if prehammer:
        base_slots += 2

    slots         = 0  # stuff related to item status will be initialized later
    t_cost        = 0
    slots_used    = 0
    slots_success = 0
    
    max_threshold = base_slots-1# min(base_slots+1, 9)
    threshold    = list(range(max_threshold))
    total_costs  = [[] for _ in range(max_threshold)]

    for thres in threshold:
        for trial in range(num_trials):
            slots         = base_slots  # start with a clean item
            t_cost        = 0
            slots_used    = 0
            slots_success = 0
            if prehammer:
                t_cost   += hammer_cost*2

            # Step 1 roll until you meet a minimum threshold of successful scrolls out of x slots
            while slots_used != slots:
                # Roll Attempt
                t_cost       += roll_cost
                slots_used    += 1
                slots_success += random.random() < success_prob

                slots_failed = slots_used - slots_success
                # Salvagable check
                # if slots - slot_used + slot_success >= threshold:
                if slots - slots_failed >= thres:
                    # still salvagable
                    continue
                else:
                    t_cost       += ark_cost
                    if prehammer:
                        t_cost   += hammer_cost*2
                    slots_used    = 0
                    slots_success = 0

            # Clean all the failed slots
            t_cost += css_cost * (slots - slots_success)
            
            # Step 1.5 (if not prehammered, do it now)
            if not prehammer:
                slots += 2
                t_cost += hammer_cost*2

            # Step 2 continue rolling and clean slate the failed slots        
            while slots_success != slots:
                # Roll Attempt
                t_cost += roll_cost
                if random.random() < success_prob:
                    # Slot roll succeeded!
                    slots_success += 1
                else:
                    # Roll failed, clean slate the failed slot
                    t_cost += css_cost

            # Step 3 record the total cost to finish
            total_costs[thres].append(t_cost)

    return total_costs

total_costs = calculate(slots,prehammer)

# Calculate the averages of each sublist
averages = np.mean(total_costs, axis=1)

# Calculate the percentiles of each sublist
percentiles = np.percentile(total_costs, [50, 68, 95, 99], axis=1)

# Format the numbers as integers with commas
def format_int(number):
    return "{:,d}".format(int(number))

# Print the results in a table
print("Index".ljust(6) + "Average".rjust(13) + "50%".rjust(13) + "68%".rjust(13) + "95%".rjust(14) + "99%".rjust(14))
for i in range(len(total_costs)):
    index_str = str(i).ljust(6)
    avg_str = format_int(averages[i]).rjust(13)
    p50_str = format_int(percentiles[0][i]).rjust(13)
    p68_str = format_int(percentiles[1][i]).rjust(13)
    p95_str = format_int(percentiles[2][i]).rjust(14)
    p99_str = format_int(percentiles[3][i]).rjust(14)
    print(f"{index_str}{avg_str}{p50_str}{p68_str}{p95_str}{p99_str}")