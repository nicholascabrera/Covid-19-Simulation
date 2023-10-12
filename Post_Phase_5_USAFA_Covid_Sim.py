import pythonGraph, random, math

'''
Pandemic Response Policy Simulation 
Author(s): Nick Cabrera(Programming + Concept) & David Hogenson(Assisted w/Concept)

drew inspiration from PEX 3 in CS110.
'''

#sim variables
window_height = 500
window_width = 1000
num_cadets = 100
cadet_radius = 12
max_velocity = 6
cadet_stats = []

cadet_qi = []
qi_time = 14 * 24

cur_sim_time = 0
infection_rate = 0.9
exposed_time = 10 * 24
infected_time = 21 * 24
num_susceptible = 0
num_exposed = 0
num_infected = 0
peak_infected = 0
num_recovered = 0

mortality_rate = 0
total_dead = 0

lung_damage_rate = 0.0005
total_lung_damaged = 0

distancing_rate = .56

mask_rate = .35

high_risk_rate = .25

quarantine_rate = .55
contact_trace_rate = .15

num_qi = 0

testing_rate = 7 * 24

sim_total = 0

# log variables
log_file = open("post_phase_5_COVID_log.csv", "w")


# --------------------------------------------------------------
# Initializes the Global Variables, and Sets Up the Simulation
# --------------------------------------------------------------
def initialize_simulation():
    global window_height, window_width, num_cadets, cadet_radius, max_velocity, cadet_stats
    global cur_sim_time, num_infected, peak_infected, mortality_rate
    global log_file
    
    pythonGraph.open_window(window_width, window_height)
    pythonGraph.set_window_title("Post Phase 5 USAFA COVID-19 Simulation")
    
    cur_sim_time = 0
    num_infected = int(num_cadets * .1) #number of cadets unknown(classified), took a guess at 10% of the wing infected.
    peak_infected = 0
    mortality_rate = 1 - 0.00000937042 #covid-19 mortality rate for cadet age group.
    
    num_mask_wearers = int(num_cadets * mask_rate)
    mask_wearers = random.sample(range(0, (num_cadets - 1)), num_mask_wearers)
    
    num_high_risk = int(num_cadets * high_risk_rate)
    high_risk_population = random.sample(range(0, (num_cadets - 1)), num_high_risk)
    
    for index in range(num_cadets):
        x_position = random.randrange(1, window_width - 1)
        y_position = random.randrange(1, window_height - 1)
        x_velocity = random.random() * max_velocity
        y_velocity = random.random() * max_velocity
        
        if (index < num_infected):
            infection_state = 'RED'
        else:
            infection_state = 'GREEN'
        
        if index in mask_wearers:
            radius = cadet_radius - 3
        else:
            radius = cadet_radius
            
#         if index in high_risk_population:
#             death_rate = 
#         else:
#             death_rate = mortality_rate
            
        
        statistics = [x_position, y_position, x_velocity, y_velocity, radius, infection_state, 0]
        cadet_stats.append(statistics)
        
    log = "DAY, SUSCEPTIBLE, EXPOSED, INFECTED, PEAK INFECTED, Q+I, DEAD, SIM TOTAL" + '\n'
    log_file.write(log)

# --------------------------------------------------------------
# calculates the distance between two objects
# --------------------------------------------------------------
def distance_from(x1, y1, x2, y2):
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance
    
def x_distance(x1, x2):
    return x2-x1

def y_distance(y1, y2):
    return y2-y1

# --------------------------------------------------------------
# Erases all simulation objects
# --------------------------------------------------------------
def erase():
    pythonGraph.clear_window('WHITE')
    

# --------------------------------------------------------------
# Updates all simulation objects
# --------------------------------------------------------------
def update():
    global cur_sim_time
    
    cur_sim_time += 1
    
    update_cadet_locations()
    update_disease_spread()
    update_spacing()
    update_seir_status()
    update_quarantine()
    update_statistics()
    update_log()
    
def update_statistics():
    global cadet_stats, num_recovered, num_infected, num_exposed, num_susceptible, peak_infected, total_dead, total_lung_damaged, cadet_qi, num_qi, sim_total
    
    num_susceptible = 0
    num_exposed = 0
    num_infected = 0
    num_recovered = 0
    total_dead = 0
    total_lung_damaged = 0
    num_qi = 0
    
    for cadet in cadet_stats:
        infection_state = cadet[5]

        if infection_state == 'GREEN':
            num_susceptible += 1
        elif infection_state == 'ORANGE':
            num_exposed += 1
        elif infection_state == 'RED':
            num_infected += 1
        elif infection_state == 'BLUE':
            num_recovered += 1
        elif infection_state == 'GRAY':
            total_lung_damaged += 1
        
        if num_infected > peak_infected:
            peak_infected = num_infected
    
    for infected in cadet_qi:
        infection_state = infected[5]
        
        if infection_state == 'BLACK':
            num_qi += 1
    
    sim_total = (num_susceptible + num_exposed + num_infected + num_qi) - total_dead

def update_seir_status():
    global cadet_stats, infection_rate, exposed_time, infected_time, cur_sim_time, mortality_rate, lung_damage_rate, total_lung_damaged
    
    for cadet in cadet_stats:
        if cadet[5] == 'ORANGE':
            if (cur_sim_time - cadet[6]) >= exposed_time:
                chance = random.random()
                if (cadet[6] < 2160):
                    if chance < (infection_rate - 0.6):
                        cadet[5] = 'RED'
                        cadet[6] = cur_sim_time
                    else:
                        cadet[5] = 'GREEN'
                        cadet[6] = 0
                else:
                    if chance < infection_rate:
                        cadet[5] = 'RED'
                        cadet[6] = cur_sim_time
                    else:
                        cadet[5] = 'GREEN'
                        cadet[6] = 0
        elif cadet[5] == 'RED':
            if (cur_sim_time - cadet[6]) >= infected_time:
                chance = random.random()
                if chance < lung_damage_rate:
                    cadet[5] = 'GREEN'
                    cadet[6] = cur_sim_time
                else:
                    total_lung_damaged += 1
                    cadet[5] = 'GRAY'

    
def update_disease_spread():
    global cadet_stats, cur_sim_time, cadet_radius
    
    for infected in cadet_stats:
        for cadet in cadet_stats:
            if infected[5] == 'RED':
                if cadet[5] == 'GREEN':
                    if distance_from(infected[0], infected[1], cadet[0], cadet[1]) < (infected[4] + cadet[4]):
                        cadet[5] = 'ORANGE'
                        cadet[6] = cur_sim_time
                
def update_cadet_locations():
    global cadet_stats, cadet_radius, distancing_rate
    
    for cadet in cadet_stats: 
        x = cadet[0]
        y = cadet[1]
        if ((x+cadet[2]) < window_width) and ((x+cadet[2]>0)):
            cadet[0] += cadet[2]
        else:
            cadet[2] *= -1
        
        if ((y+cadet[3]) < window_height) and ((y+cadet[3]) > 0):
            cadet[1] += cadet[3]
        else:
            cadet[3] *= -1

def update_spacing():
    global cadet_stats, cadet_radius, distancing_rate
    social_distance = 2 * cadet_radius + 6
    
    for infected in cadet_stats:
        for cadet in cadet_stats:
            if (infected[5] == 'RED'):
                if cadet[5] == 'GREEN':
                    if distance_from(infected[0], infected[1], cadet[0], cadet[1]) < social_distance:
                        chance = random.random()
                        if chance < distancing_rate:
                            if(x_distance(infected[0], cadet[0]) > 0):
                                cadet[2] = math.fabs(cadet[2])
                            else:
                                cadet[2] = math.fabs(cadet[2]) * (-1)
                            if(y_distance(infected[1], cadet[1]) > 0):
                                cadet[3] = math.fabs(cadet[3])
                            else:
                                cadet[3] = math.fabs(cadet[3]) * (-1)
                                
def update_quarantine():
    global cadet_stats, cadet_qi, quarantine_rate, contact_trace_rate, cur_sim_time, qi_time
    
    for cadet in cadet_stats:
        if (((cur_sim_time) % testing_rate) == 0) and (cur_sim_time) != 0:
            if cadet[5] == 'RED':
                chance = random.random()
                if chance < quarantine_rate:
                    cadet[5] = 'BLACK'
                    cadet[6] = cur_sim_time
                    cadet_qi.append(cadet)
                    cadet_stats.remove(cadet)
            if cadet[5] == 'ORANGE':
                chance = random.random()
                if chance < contact_trace_rate:
                    cadet[5] = 'BLACK'
                    cadet[6] = cur_sim_time
                    cadet_qi.append(cadet)
                    cadet_stats.remove(cadet)
#             if cadet[5] == 'BLACK':
#                 if (cur_sim_time - cadet[6]) > qi_time:
#                     cadet[5] = 'GREEN'
#                     cadet[6] = 0
    
    for infected in cadet_qi:
        if (cur_sim_time - infected[6]) > qi_time:
            infected[5] = 'GREEN'
            infected[6] = 0
            cadet_stats.append(infected)
            cadet_qi.remove(infected)

def update_log():
    global num_infected, num_exposed, num_susceptible, total_dead, num_qi, sim_total, peak_infected, cur_sim_time, log_file
    
    log_sim_day = (str(int(cur_sim_time/24)))
    log_susceptible = str(num_susceptible) + "(" + str(round(((num_susceptible/sim_total)*100), 1)) + "%)"
    log_exposed = str(num_exposed) + "(" + str(round(((num_exposed/sim_total)*100), 1)) + "%)"
    log_infected = str(num_infected) + "(" + str(round(((num_infected/sim_total)*100), 1)) + "%)"
    log_peak_infected = str(peak_infected) + "(" + str(round(((peak_infected/sim_total)*100), 1)) + "%)"
    log_qi = str(num_qi) + "(" + str(round(((num_qi/sim_total)*100), 1)) + "%)"
    log_dead = str(total_dead) + "(" + str(round(((total_dead/(sim_total+total_dead))*100), 1)) + "%)"
    log_sim_total = str(sim_total)
    
    log = log_sim_day+" ,"+log_susceptible+", "+log_exposed+", "+log_infected+ ", "+log_peak_infected+", "+log_qi+", "+log_dead+", "+log_sim_total+'\n'
    if ((cur_sim_time % (7 * 24)) == 0) :
        log_file.write(log)    

# --------------------------------------------------------------
# Draws all simulation objects
# --------------------------------------------------------------
def draw():    
    global cadet_stats, num_infected, num_exposed, num_susceptible, peak_infected, cur_sim_time, total_dead, num_qi, sim_total, total_lung_damaged
    
    for cadet in cadet_stats:
        pythonGraph.draw_circle(cadet[0], cadet[1], cadet[4], cadet[5], True)
    
    sim_day = 'Sim Day: ' + str(int(cur_sim_time / 24))
    pythonGraph.draw_text(sim_day, 0, 0, 'BLACK', 20)
    
    num_sus = 'Susceptible (Green): ' + str(num_susceptible)
    pythonGraph.draw_text(num_sus, 0, 22, 'BLACK', 20)
    
    num_expo = 'Exposed (Orange): ' + str(num_exposed)
    pythonGraph.draw_text(num_expo, 0, 42, 'BLACK', 20)
    
    num_inf = 'Infected (Red): ' + str(num_infected)
    pythonGraph.draw_text(num_inf, 0, 62, 'BLACK', 20)
    
    peak_inf = 'Peak Infected: ' + str(peak_infected)
    pythonGraph.draw_text(peak_inf, 0, 82, 'BLACK', 20)
    
    num_QI = 'Cadets Quarantined: ' + str(num_qi)
    pythonGraph.draw_text(num_QI, 0, 102, 'BLACK', 20)
    
    tot_damaged = 'Total Lung Damaged: ' + str(total_lung_damaged)
    pythonGraph.draw_text(tot_damaged, 0, 122, 'BLACK', 20)
    
    total = 'Simulation Total: ' + str(sim_total)
    pythonGraph.draw_text(total, 0, 142, 'BLACK', 20)


# -----------------------------------------------------
# Main Program
# This is what actually runs when you press Play
# -----------------------------------------------------
random.seed()
initialize_simulation()

while pythonGraph.window_not_closed():
    erase()
    draw()
    update()
    pythonGraph.update_window()

log_file.close()
pythonGraph.close_window()