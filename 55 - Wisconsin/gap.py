import tempfile, tarfile, operator, os, shutil

def iterate_plans(filename):
    '''
    '''
    dirname = tempfile.mkdtemp(prefix='plans-')

    with tarfile.open(filename, 'r:gz') as file:
        for member in sorted(file, key=operator.attrgetter('path')):
            if member.isreg():
                file.extract(member, path=dirname)
                filepath = os.path.join(dirname, member.path)
                with open(filepath) as plan:
                    print(member.path)
                    yield [int(i) for i in plan.read().split()]
                os.remove(filepath)
    
    shutil.rmtree(dirname)

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
    
    return (wasted_blue - wasted_red) / election_votes
        
    print(int(blue_wins), 'blue and', int(red_wins), 'red districts')
    print(int(election_votes), 'total votes')
    print(int(wasted_red), 'wasted red votes')
    print(int(wasted_blue), 'wasted blue votes')
    
    if wasted_blue > wasted_red:
        print('+{:.1f}% gap for red team'.format(100 * (wasted_blue - wasted_red) / election_votes))
    else:
        print('+{:.1f}% gap for blue team'.format(100 * (wasted_red - wasted_blue) / election_votes))
