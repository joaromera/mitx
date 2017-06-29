# Mainly an introduction to classes in Python for MITx @ EDX.org

import math
from operator import itemgetter, attrgetter, methodcaller

class AdoptionCenter:
    """
    The AdoptionCenter class stores the important information that a
    client would need to know about, such as the different numbers of
    species stored, the location, and the name. It also has a method to adopt a pet.
    """
    def __init__(self, name, species_types, location):
        self.name = name
        self.species_types = species_types
        locationTemp = (float(location[0]), float(location[1]))
        self.location = locationTemp
    def get_number_of_species(self, animal):
        if animal in self.species_types.keys():
            return self.species_types[animal]
        else:
            return 0
    def get_location(self):
        return self.location
    def get_species_count(self):
        species_count = self.species_types.copy()
        return species_count
    def get_name(self):
        return self.name
    def adopt_pet(self, species):
        if species in self.species_types.keys():
            if self.species_types[species] > 0:
                self.species_types[species] = self.species_types[species] - 1
                if self.species_types[species] == 0:
                    del self.species_types[species]

class Adopter:
    """
    Adopters represent people interested in adopting a species.
    They have a desired species type that they want, and their score is
    simply the number of species that the shelter has of that species.
    """
    def __init__(self, name, desired_species):
        self.name = name
        self.desired_species = desired_species
    def get_name(self):
        return self.name
    def get_desired_species(self):
        return self.desired_species
    def get_score(self, adoption_center):
        return 1.0 * adoption_center.get_number_of_species(self.desired_species)


class FlexibleAdopter(Adopter):
    def __init__(self, name, desired_species, considered_species):
        self.name = name
        self.desired_species = desired_species
        self.considered_species = considered_species
    def get_score(self, adoption_center):
        original = 1.0 * adoption_center.get_number_of_species(self.desired_species)
        numberConsidered = 0
        for i in self.considered_species:
            numberConsidered += adoption_center.get_number_of_species(i)
        return original + 0.3 * numberConsidered


class FearfulAdopter(Adopter):
    def __init__(self, name, desired_species, feared_species):
        self.name = name
        self.desired_species = desired_species
        self.feared_species = feared_species
    def get_score(self, adoption_center):
        original = 1.0 * adoption_center.get_number_of_species(self.desired_species)
        score = original - 0.3 * adoption_center.get_number_of_species(self.feared_species)
        if score > 0:
            return score
        else:
            return 0.0


class AllergicAdopter(Adopter):
    def __init__(self, name, desired_species, allergic_species):
        self.name = name
        self.desired_species = desired_species
        self.allergic_species = allergic_species
    def get_score(self, adoption_center):
        for i in self.allergic_species:
            if i in adoption_center.get_species_count():
                return 0.0
        return 1.0 * adoption_center.get_number_of_species(self.desired_species)


class MedicatedAllergicAdopter(AllergicAdopter):
    def __init__(self, name, desired_species, allergic_species, medicine_effectiveness):
        self.name = name
        self.desired_species = desired_species
        self.allergic_species = allergic_species
        self.medicine_effectiveness = medicine_effectiveness
    def get_score(self, adoption_center):
        animalsThere = []
        for i in self.allergic_species:
            if i in (adoption_center.get_species_count()).keys():
                animalsThere += [i]
        lowestEffect = 1.0
        for i in animalsThere:
            if i in self.medicine_effectiveness.keys():
                if self.medicine_effectiveness[i] < lowestEffect:
                    lowestEffect = self.medicine_effectiveness[i]
        return lowestEffect * adoption_center.get_number_of_species(self.desired_species)


class SluggishAdopter(Adopter):
    def __init__(self, name, desired_species, location):
        self.name = name
        self.desired_species = desired_species
        self.location = location
    def get_linear_distance(self, xy):
        xDistance = (xy[0] - self.location[0])
        yDistance = (xy[1] - self.location[1])
        distance = math.sqrt((xDistance * xDistance) + (yDistance * yDistance))
        return distance
    def get_score(self, adoption_center):
        distance = self.get_linear_distance(adoption_center.get_location())
        if distance < 1:
            return 1.0 * adoption_center.get_number_of_species(self.desired_species)
        elif distance == 1 or distance < 3:
            return random.uniform(0.7, 0.9) * adoption_center.get_number_of_species(self.desired_species)
        elif distance == 3 or distance < 5:
            return random.uniform(0.5, 0.7) * adoption_center.get_number_of_species(self.desired_species)
        elif distance == 5 or distance > 5:
            return random.uniform(0.1, 0.5) * adoption_center.get_number_of_species(self.desired_species)


def get_ordered_adoption_center_list(adopter, list_of_adoption_centers):
    lista = []
    for i in list_of_adoption_centers:
        lista += [(adopter.get_score(i), i.get_name(), i)]
    lista_sorted = sorted(lista, key=itemgetter(0), reverse=True)
    output = []
    for i in lista_sorted:
        output += [i[2]]
    return output

def get_adopters_for_advertisement(adoption_center, list_of_adopters, n):
    lista = []
    for i in list_of_adopters:
        lista += [(i.get_score(adoption_center), i.get_name(), i)]
    lista_sorted = sorted(lista, key=itemgetter(0), reverse=True)
    for i in range(len(lista_sorted)):
        for i in range(len(lista_sorted)):
            try:
                if lista_sorted[i][0] == lista_sorted[i + 1][0]:
                    if lista_sorted[i][1] > lista_sorted[i + 1][1]:
                        lista_sorted[i], lista_sorted[i + 1] = lista_sorted[i + 1], lista_sorted[i]
            except IndexError:
                pass
    output = []
    for i in lista_sorted:
        output += [i[2]]
    return output[:n]
