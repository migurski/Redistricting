from osgeo import ogr
import sys

def main(plan_path):
    '''
    '''
    plan_ds = ogr.Open(plan_path)
    plan_lyr = plan_ds.GetLayer(0)
    
    votes_total, wasted_red, wasted_blue = 0, 0, 0
    
    for feature in plan_lyr:
        red_votes, blue_votes = feature.GetField('pres_red'), feature.GetField('pres_blue')
        district_votes = red_votes + blue_votes
        
        if red_votes > blue_votes:
            wasted_blue += blue_votes
            wasted_red += red_votes - (district_votes / 2)
        elif blue_votes > red_votes:
            wasted_red += red_votes
            wasted_blue += blue_votes - (district_votes / 2)
        else:
            raise ValueError('Unlikely 50/50 split')
        
        votes_total += red_votes
        votes_total += blue_votes
    
    print(int(votes_total), 'total votes')
    print(int(wasted_red), 'wasted red votes')
    print(int(wasted_blue), 'wasted blue votes')
    
    if wasted_blue > wasted_red:
        print('+{:.1f}% gap for red team'.format(100 * (wasted_blue - wasted_red) / votes_total))
    else:
        print('+{:.1f}% gap for blue team'.format(100 * (wasted_red - wasted_blue) / votes_total))

if __name__ == '__main__':
    _, plan_path = sys.argv
    exit(main(plan_path))
