import os

def getRoleImages():
  """Get all the role images."""
  aRoles = []

  for dirname, dirnames, filenames in os.walk('./static/img/roles/'):
    # print path to all filenames.
    for filename in filenames:
      aRoles.append(filename)

  aRoles.sort()
  return aRoles


if __name__ == '__main__':
    print getRoleImages()