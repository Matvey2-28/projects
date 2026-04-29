import solver
import parser
import create_xdmf
import sys 


def main(data_path: str, output_path: str) -> None:
    print('Запуск main.', '\n')
    model_data = parser.Parser(data_path)
    model_solver = solver.Solver(model_data)
    model_solver.solve(output_path)
    


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2])
    main('./input.json', './output.hdf5')