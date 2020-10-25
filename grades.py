from argparse import ArgumentParser
import pandas as pd

def graderead(path: str) -> pd.DataFrame:
	grades = pd.read_html(path, index_col=0, header=0)[0]
	grade_name = 'Grade' if 'Grade' in grades.head() else 'Karakter'
	grades['gradepoint'] = [grade.split()[0] for grade in grades[grade_name]]
	# Handle grades such as BE by coercing to NaN
	grades['gradepoint'] = pd.to_numeric(grades.gradepoint, errors='coerce')
	# Weighting grade with normalized ECTS point weight where NaN subjects are not considered
	grades['weightedgrade'] = grades.gradepoint*grades.ECTS/grades[grades.gradepoint.notnull()]['ECTS'].mean()
	return grades

def describe(grades: pd.DataFrame):
	prettiboiline = '\n'+''.join('-' for _ in range(100))

	print(f"Fetched grades", prettiboiline)
	print(grades, prettiboiline)
	print(f"Stats for simple and weighted means", prettiboiline)
	print(grades[['gradepoint', 'weightedgrade']].describe())

	print(f"Mean grade is thus {float( grades[['weightedgrade']].mean() ):.3f}")

if __name__ == '__main__':
	ap = ArgumentParser(description="Get the D A T A and the means from inside grades")
	ap.add_argument('htmlfile', type=str, metavar='FILE', help="Your html file downloaded from "
			"https://cn.inside.dtu.dk/cnnet/Grades/Grades.aspx")
	ap.add_argument('--outfile', type=str, metavar='FILE', help="Filename to save grades", default='mygrades.csv')
	args = ap.parse_args()

	grades = graderead(args.htmlfile)
	describe(grades)

	# Add mean to the bottom for readability
	grades.loc['Mean'] = grades.mean()
	grades.to_csv(args.outfile, index=False)
