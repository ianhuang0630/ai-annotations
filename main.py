import argparse
from assign_score import assign
from cleanup import cleanup

def main(args):
    
    annotated = assign(
        args.input_dir,
        args.annotation_dir,
        args.prompt
    ) 

    output_csv = cleanup(
        args.annotation_dir,
        args.output_csv
    )

    return output_csv
    


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser( description = "") 
    parser.add_argument(
        "-i", "--input-dir",
        type=str,
        required=True,
        help="Path to the data to be annotated",
    )
         
    parser.add_argument(
        "-a", "--annotation-dir",
        type=str,
        required = True,
        help="Path to the output annotations"
    )
        
    parser.add_argument(
        "-p",  "--prompt",
        type=str,
        required=True,
        help="Path to prompt .txt"
    )


    parser.add_argument(
        "-c",  "--output-csv",
        type=str,
        required=True,
        help="Path to output CSV"
    )


    args = parser.parse_args()

    main(args)

        
    pass