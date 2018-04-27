import numpy as np

import Constants as c


class AI:
    
    
    def getAction(self, PP):
        
        if PP == 0:
            return 1
        else:
            return np.random.choice(c.actions)

#