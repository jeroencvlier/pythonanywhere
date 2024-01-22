
import subprocess
import os



def aws_sync():
    list_of_options_per_week_on_cloud = os.listdir('/home/jeroencvlier/option_chain_data/')
    list_of_options_per_week_on_cloud = [x for x in list_of_options_per_week_on_cloud if '_week_' in x]

    for week in sorted(list_of_options_per_week_on_cloud,reverse = True):
        print(f'Pulling Option Data for {week}!')
        aws_command = ['/home/jeroencvlier/.virtualenvs/awssync/bin/aws', 's3', 'sync', f'/home/jeroencvlier/option_chain_data/{week}/', 's3://option-chain-data-backup/option_chain_data', '--size-only', '--exclude', '"*"', '--include', '*.json.gz', '--profile', 'default']

        try:
            subprocess.run(aws_command, check=True, text=True)

        except subprocess.CalledProcessError as e:
            print("Error:")
            print(e.stderr)
            
            
            

if __name__ == '__main__':
    aws_sync()
    