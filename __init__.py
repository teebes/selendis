"""
Run on prod:

In [22]: for mob in Mob.objects.all():
   ....:   mob.static = False
   ....:   mob.save()
   
"""