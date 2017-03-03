from osgeo import ogr
import sys

def calc(districts):
    '''
    '''
    election_votes, wasted_red, wasted_blue, red_wins, blue_wins = 0, 0, 0, 0, 0
    
    for district in districts:
        red_votes = [float(v) for (k, v) in district.items() if 'red' in k.lower()][0]
        blue_votes = [float(v) for (k, v) in district.items() if 'blu' in k.lower()][0]
        district_votes = red_votes + blue_votes
        election_votes += district_votes
        win_threshold = district_votes / 2
    
        if red_votes > blue_votes:
            red_wins += 1
            wasted_red += red_votes - win_threshold # surplus
            wasted_blue += blue_votes # loser
        elif blue_votes > red_votes:
            blue_wins += 1
            wasted_blue += blue_votes - win_threshold # surplus
            wasted_red += red_votes # loser
        else:
            raise ValueError('Unlikely 50/50 split')
        
    print(int(blue_wins), 'blue and', int(red_wins), 'red districts')
    print(int(election_votes), 'total votes')
    print(int(wasted_red), 'wasted red votes')
    print(int(wasted_blue), 'wasted blue votes')
    
    if wasted_blue > wasted_red:
        print('+{:.1f}% gap for red team'.format(100 * (wasted_blue - wasted_red) / election_votes))
    else:
        print('+{:.1f}% gap for blue team'.format(100 * (wasted_red - wasted_blue) / election_votes))

def main(plan_path):
    '''
    '''
    plan_ds = ogr.Open(plan_path)
    plan_lyr = plan_ds.GetLayer(0)
    
    defn = plan_lyr.GetLayerDefn()
    names = {defn.GetFieldDefn(i).name for i in range(defn.GetFieldCount())}
    districts = [{n: feat.GetField(n) for n in names} for feat in plan_lyr]
    
    return calc(districts)

if __name__ == '__main__':
    _, plan_path = sys.argv
    exit(main(plan_path))
