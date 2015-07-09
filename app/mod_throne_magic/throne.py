import random

class Throne:
  myD = {
    "Angel": (0, [2,3,4,6,7,11,12,13,16], [2,3,4,6,7,9,11,12,13,15]),
    "Barbarian": (1, [5,7,10,11,12,13], [3,4,6,7,9,12,16]),
    "Cultist": (2, [0,4,5,8,10], [4,5,6,7,8,9,10,12,15,16]),
    "Demon": (3, [0,1,4,5,6,7,8,9,10,12,14,15], [4,5,6,7,8,9,10,12,15]),
    "Dragon": (4, [0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16], [2,3,5,8,9,10,11,12,13,14,15,16]),
    "King's Bannerman": (5, [2,3,4,6,7,11,12,13,16], [1,2,3,4,6,7,9,11,12,13,15,16]),
    "Ogre": (6, [0,1,2,3,5,8,9,10,11,13,14,15,16], [3,4,5,8,9,10,11,12,13,14,15,16]),
    "Ogre King": (7, [0,1,2,3,5,8,9,10,11,13,14,15,16], [1,3,4,5,8,10,11,12,13,14,15,16]),
    "Priest": (8, [2,3,4,6,7,11,12,13,16], [2,3,4,6,7,9,11,12,13,15,16]),
    "Reaver": (9, [0,1,2,3,4,5,6,8,10,11,13,14,15,16], [3,4,6,7,12,16]),
    "The King": (10, [2,3,4,6,7,11,12,13,16], [1,2,3,4,6,7,9,11,12,13,14,15,16]),
    "The Usurper": (11, [0,4,5,6,7,8,10,12], [1,4,5,6,7,8,9,10,12,14,15,16]),
    "Titan": (12, [0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,16], [1,3,4,5,8,10,11,13,14,15,16]),
    "Usurper's Bannerman": (13, [0,4,5,6,7,8,10,12,], [1,4,5,6,7,8,9,10,12,15,16]),
    "Vengeant": (14, [4,6,7,10,11,12,], [3,4,6,7,9,12,16]),
    "Wizard": (15, [0,2,3,4,5,6,7,8,10,11,12,13,16], [3,4,6,7,9,12,16]),
    "Wraith": (16, [1,2,4,5,6,7,8,9,10,11,12,13,14,15,], [4,5,6,7,8,9,10,12,15])
  }

  myThrones = [
    "Throne of Power",
    "Throne of the Abyss",
    "Throne of the Ancient Kings",
    "Throne of the Spider Queen",
    "Throne of Tyrants",
    "Throne of Visions",
    "Throne of Wisdom"
  ]
  myHoldings = [
    "Balmecia", "Bolgirn", "Calanar, City of Sorcerers", "Esseldell", "Farmhold",
    "Forth", "Galdi", "Ironhall", "Ixenverthicha", "Myrvanna", "Scarheim",
    "The Black Citadel", "The Grey Citadel", "The Norjak", "The Shadowlands",
    "The White Citadel", "Ultar"
  ]
  mySeasons = ["Spring", "Summer", "Autumn", "Winter"]

  mySel = []

  myMustEliminate = []
  myEliminatedBy = []
  myAllowed = []

  def getTruism(self, theIndex, theRole):
    """Check the truism of a valid value."""
    # Checks for the index in the ones they must eliminate.
    aWinCheck = theIndex in self.myMustEliminate

    # Checks for the index in the ones that have to eliminate them.
    aLoseCheck = theIndex in self.myEliminatedBy

    # # God damn angel check.
    aAngelCheck = True

    # Check for the emptiness of BOTH lists.
    aEmptyCheck = not self.myMustEliminate and not self.myEliminatedBy

    return (aWinCheck and aLoseCheck) or aAngelCheck or aEmptyCheck

  def selectRole(self, theRole):
    # Get the proper entry.
    aIndex = self.myD[theRole][0]

    # Check to see if it's allowed.
    if self.getTruism(aIndex, theRole):
      # If so, add it.
      self.mySel.append(theRole)

      # Add the new role to "must eliminate" list.
      self.myMustEliminate = list(set(self.myMustEliminate + self.myD[theRole][1]))

      # Add the new role to "eliminated by" list.
      self.myEliminatedBy = list(set(self.myEliminatedBy + self.myD[theRole][2]))

      # Remove the current id from each list, just to avoid weirdness.
      try:
        self.myMustEliminate.remove(aIndex)
      except ValueError:
        pass

      try:
        self.myEliminatedBy.remove(aIndex)
      except ValueError:
        pass

      # Set up a helper list, which contains all the roles allowed.
      self.myAllowed = list(set(self.myMustEliminate) & set(self.myEliminatedBy))

      # Return True if it's good.
      return True

    # If there is an error return False.
    return False

  def getRandom(self, theLimit):
    aEntry = None
    aLastRole = None
    aCount = 0

    while True:
      aEntry = random.choice(self.myD.keys())

      # Break on specific input.
      if aCount >= theLimit:
        # return list(self.myD[aRole][0] for aRole in self.mySel)
        return self.mySel
      elif isinstance(aEntry, str) and aEntry in self.myD and aEntry not in self.mySel:
        aLastRole = aEntry

        if self.selectRole(aEntry):
          aCount += 1

def main():
  aThrone = Throne()

  aEntry = None
  aLastRole = None

  while True:
    print "Already selected roles:"
    if aLastRole:
      for aItem in aThrone.mySel:
        print aItem
      print
    else:
      print "None\n"

    print "Available roles:"
    if aLastRole:
      aRet = []
      for aRole, aAttr in aThrone.myD.iteritems():
        if aAttr[0] in aThrone.myAllowed:
          print aRole
      print
    else:
      print "All\n"

    aEntry = raw_input("Enter a command [" + str(aLastRole) + "]: ")

    # Break on specific input.
    if aEntry == "quit":
      print "!! Quitting."
      return
    elif isinstance(aEntry, str) and aEntry in aThrone.myD and aEntry not in aThrone.mySel:
      aLastRole = aEntry

      if not aThrone.selectRole(aEntry):
        print "-- Command " + aEntry + " has is not valid.\n"
    elif aEntry in aThrone.mySel:
      print "-- Command " + str(aEntry) + " already selected.\n"
    else:
      print "-- Command " + str(aEntry) + " not recognized.\n"

    print "\n================================================================================\n"


if __name__ == '__main__':
  main()
