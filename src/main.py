import random
import pandas as pd
import numpy as np
import argparse

def get_parameters_sim1():
    sim_name = "sim1"
    num_sims = 1000
    num_women = 500  
    num_men = 500 
    profiles_per_day_men = 100
    profiles_per_day_women = 100
    like_percentage_men = 0.25 
    like_percentage_women = 0.25 
    include_attractiveness = False
    return sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness


def get_parameters_sim2():
    sim_name = "sim2"
    num_sims = 1000
    num_women = 333  
    num_men = 667 
    profiles_per_day_men = 100
    profiles_per_day_women = 100
    like_percentage_men = 0.25 
    like_percentage_women = 0.25 
    include_attractiveness = False
    return sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness


def get_parameters_sim3():
    sim_name = "sim3"
    num_sims = 1000
    num_women = 333  
    num_men = 667 
    profiles_per_day_men = 100
    profiles_per_day_women = 100
    like_percentage_men = 0.46 
    like_percentage_women = 0.14  
    include_attractiveness = False
    return sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness


def get_parameters_sim4():
    sim_name = "sim4"
    num_sims = 1000
    num_women = 333 
    num_men = 667  
    profiles_per_day_men = 100
    profiles_per_day_women = 100
    like_percentage_men = 0.46  
    like_percentage_women = 0.14  
    include_attractiveness = True
    return sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness


class User:
    def __init__(self, id, gender, profiles_per_day, like_percentage, include_attractiveness):
        self.id = id
        self.gender = gender
        self.profiles_per_day = profiles_per_day
        self.like_percentage = like_percentage
        self.likes = 0
        self.matches = 0
        self.swipes = 0  # nr of times the profile was swiped by other users
        self.attractiveness = random.random()
        self.users_like_sent = []
        self.users_like_received = []
        self.include_attractiveness = include_attractiveness

    def swipe(self, other_user):
        other_user.swipes += 1
        random_number = random.random()
        prob = self.get_like_prob(other_user)
        # prob = other_user.attractiveness * self.like_percentage
        if random_number <= prob:
            # Like:
            other_user.likes += 1
            other_user.users_like_received.append(self.id)
            self.users_like_sent.append(other_user.id)
            if self.id in other_user.users_like_sent:
                # Match
                self.matches += 1
                other_user.matches += 1

    def get_like_prob(self, other_user):
        if user.include_attractiveness:
            # # polynomial:
            like_prob = other_user.attractiveness ** (1/self.like_percentage-1)

        else:
            like_prob = self.like_percentage
        return like_prob


# Initialize KPIs
user_gender_total = []
user_likes_total = []
user_matches_total = []
user_attractiveness_total = []

user_likes_means = []
user_matches_means = []

user_likes_medians = []
user_matches_medians = []


# Define argparse
parser = argparse.ArgumentParser(description='Run a simulation.')
parser.add_argument('-p', '--simulation', type=str, help='Name of the simulation to run', default='sim1')
args = parser.parse_args()

# Define simulation parameters
if args.simulation == 'sim1':
    sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness = get_parameters_sim1()
elif args.simulation == 'sim2':
    sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness = get_parameters_sim2()
elif args.simulation == 'sim3':
    sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness = get_parameters_sim3()
elif args.simulation == 'sim4':
    sim_name, num_sims, num_women, num_men, profiles_per_day_men, profiles_per_day_women, like_percentage_men, like_percentage_women, include_attractiveness = get_parameters_sim4()
else:
    raise Exception('Simulation not found')    


# Run Sims
for sim in range(0, num_sims):
    print("Sim %s/%s" % (str(sim+1), num_sims))
    users_female = [User(user, 'FEMALE', profiles_per_day_women, like_percentage_women, include_attractiveness) for user in range(0, num_women)]
    users_male = [User(user, 'MALE', profiles_per_day_men, like_percentage_men, include_attractiveness) for user in range(num_women, num_women + num_men)]
    users = users_female + users_male

    # Match users:
    users_female_swipes = [(user.id, user.swipes) for user in users_female]
    users_male_swipes = [(user.id, user.swipes) for user in users_male]
    for user in users_female:
        users_male_swipes = [(user.id, user.swipes) for user in users_male]
        users_male_swipes.sort(key=lambda x: x[1])
        swipe_count = 0
        for (user_male_id, user_male_swipes) in users_male_swipes:
            user_male = users[user_male_id]
            if swipe_count < profiles_per_day_women:
                user.swipe(user_male)
            else:
                break
            swipe_count += 1
    for user in users_male:
        users_female_swipes = [(user.id, user.swipes) for user in users_female]
        users_female_swipes.sort(key=lambda x: x[1])
        swipe_count = 0
        # start with other users who already liked the user:
        for user_female_id in user.users_like_received:
            user_female = users[user_female_id]
            if swipe_count < profiles_per_day_men:
                user.swipe(user_female)
            else:
                break
            swipe_count += 1
        # remaining users:
        for (user_female_id, user_female_swipes) in users_female_swipes:
            if swipe_count < profiles_per_day_men:
                if user_female_id not in user.users_like_received:
                    user_female = users[user_female_id]
                    user.swipe(user_female)
                    swipe_count += 1
            else:
                break

    # Update KPIs:
    user_gender = [user.gender for user in users]
    user_likes = [user.likes for user in users]
    user_matches = [user.matches for user in users]
    user_attractiveness = [user.attractiveness for user in users]

    user_gender_total += user_gender
    user_likes_total += user_likes
    user_matches_total += user_matches
    user_attractiveness_total += user_attractiveness

    user_likes_means.append(np.mean(user_likes))
    user_matches_means.append(np.mean(user_matches))

    user_likes_medians.append(np.median(user_likes))
    user_matches_medians.append(np.median(user_matches))


df = pd.DataFrame()
df['gender'] = user_gender_total
df['attractiveness'] = user_attractiveness_total
df['likes'] = user_likes_total
df['matches'] = user_matches_total
df.to_csv('../results/results_'+sim_name+'.csv')

