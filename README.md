*This project has been created as part of the 42 curriculum by msumiji and ssagano*

# Description
In this project, we will do the following:<br>
・Generate a random maze based on the information specified in config.txt.<br>
・Place the number “42” in the center of the maze. The maze should be generated so that it avoids this number.<br>
・Display the start and goal positions, and show the shortest path from the start to the goal.<br>
In this project, dead ends (locations surrounded by walls on three sides) are also eliminated in imperfect mazes (excluding the location of the “42” character).<br>

## About config.txt
This file configures the parameters for generating a maze.<br>
WIDTH: The width of the maze<br>
HEIGHT: The height of the maze<br>
Setting PERFECT to True generates a perfect maze; setting it to False generates an imperfect maze.<br>
ENTRY = The coordinates of the starting point<br>
OUTPUT_FILE = The file that stores the text information of the generated maze.<br>
EXIT = Coordinates of the exit<br>
SEED = The number used as the source for random number generation. If the SEED value is the same, the same maze will always be generated; however, selecting “regenerate” with the same SEED value will produce a different maze. The order in which these mazes are generated is always the same when the SEED value is identical.<br>

## Algorithm
### Maze Generation
　Maze generation uses an algorithm called depth-first search (DFS). In this method, the program moves from the starting point to an adjacent unvisited cell and removes the wall in the direction of movement to create a path. This algorithm is explained below in accordance with the code for this project.<br>
1. Initialize all cells as walls (line 175-178).<br>
2. Place the character “42” (lines 179, 181).<br>
3. Manage visited cells (line 183-186).<br>
4. Start DFS from the starting point (lines 196, 197).<br>
5. Search for adjacent unvisited cells (lines 202–209).<br>
6. Randomly select one and remove the wall (lines 212–214).<br>
7. Mark the destination as visited and add it to the stack (lines 215, 216).<br>
8. If a dead end is reached, return (lines 217, 218).<br>

　Another well-known algorithm for generating mazes is the “digging method.” In this method, a hole is dug from the starting point, and the program advances two squares at a time through unvisited areas. Consequently, the maze must have an odd number of rows and columns. Since this method cannot handle cases where the number of rows or columns is even as specified in config.txt, we determined it would be difficult to apply to this project; therefore, we adopted the DFS algorithm described above.

### Maze Exploration
To find the shortest path through the maze, I used a method called breadth-first search (BFS). This method finds the shortest path by following the steps below.
1. Starting from the starting point, look for a location one square away. If there are multiple such locations, register all of them in a dictionary.
2. Next, search for squares to which the player can move. If there are multiple options, add them all to the dictionary. For example, if two squares are found during the first move, and each of those allows for two possible moves in the next step, a total of four squares will be added to the dictionary during the second move.
3. If the goal is found, the process ends. Since the process ends as soon as the goal is found along any of the multiple paths, the path along which the goal was found first is the shortest path.
4. Reconstruct the shortest path by tracing the information recorded in the dictionary.

Another method for finding the shortest path is A* search. While this method can search faster than BFS for large mazes, the algorithm is complex; for small mazes like the one in this project, we determined that BFS is sufficient.

## Roles
  msumiji: Creating README.md, reviewing and revising the code.<br>
  ssagano: Writing the main body of the code, creating LICENSE.md.<br>

## Reflections on the Project
　This team was formed in August. However, since this project involved using a virtual environment, we decided to wait until one of the members had finished “python08,” so we didn’t actually get started until late October. Initially, since msumiji had finished Python08 first, the plan was for msumiji to take the lead on coding. However, since ssagano had a better understanding of the virtual environment, ssagano ended up taking the lead on coding.<br>
　We struggled to balance eliminating dead ends with avoiding the creation of 3×3 open spaces. For a dead end blocked on three sides, we devised an algorithm that randomly selects and removes one of the three walls, but we also considered whether this might create a 3×3 open space. After drawing diagrams, I found it difficult to conceive of an example where removing a single wall from an overlapping dead-end would create an open space. Furthermore, after actually constructing an incomplete maze, I confirmed that no open spaces were created. Therefore, even without a rigorous proof, we concluded that open spaces cannot be formed.<br>

## Strengths and Areas for Improvement
One area for improvement is making the shortest route easier to understand. Currently, it’s simply indicated by dots, but I think it would be even better if it were shown with arrows to make it clearer. Furthermore, I think it would be even better if the maze route were turned into a video that, when played, guides the player from the start to the finish.

## Special Tools Used
while the use of a virtual environment was strongly recommended for this project, I believe there was no point in using one since I relied solely on Python’s standard library.

# Instruction
make install: Installs the virtual environment. Run this command first before executing any other commands.

make run: Runs the program. When executed, a maze is displayed. Four options are also displayed simultaneously. Entering each number will execute the corresponding option. Selecting 1 generates a different maze. If the SEED value is fixed, the system is designed so that different mazes are always displayed in the same order. For example, if SEED is set to 42, selecting “Re-generate a new maze” will generate mazes in the order Maze A → Maze B → Maze C. However, if SEED is set to 41, the mazes will be generated in the order Maze D → Maze E → Maze F.

make debug: Uses pdb, the standard Python debugger. This allows you to execute the program one line at a time.

make clean: Deletes temporary files such as those created for the virtual environment and mypy_cache.

make lint: Runs checks using flake8 and mypy.  If you run `make lint-strict`, it will execute `mypy --strict .` simultaneously with flake8.

# Code Reusability
The maze program in this project is implemented as an independent, reusable module (`mazegen`) that can be imported and used in future projects. For example, consider using this project’s maze program in a Pac-Man game. In this case, all parts except those related to drawing the maze and displaying the interactive menu can be reused (via `.venv`). Specifically, these are the `render`, `export`, and `run_interactive` methods of the `MazeGenerator` class. The following explains how to import this program

## 1. How to Build the Package
When you run the `install` rule in the Makefile, the `build` and `wheel` packages are automatically installed within the virtual environment. You can use this to build the package and generate a `.whl` file using the following command:

### Install dependencies (includes build and wheel)
make install

### Activate the virtual environment and build the package
make build

If the build is successful, a `dist/` directory will be created in the root directory, and a Wheel file will be generated.
Example: `dist/mazegen-1.0.0-py3-none-any.whl`

## 2. Installing and Using the Package
You can install the generated .whl file into any virtual environment or project using pip.
pip install dist/mazegen-1.0.0-py3-none-any.whl

# Resources
In creating this project, we drew on advice from students who entered the program at the same time as us. We happened to have many opportunities to review a_maze_ing, and during those sessions, they explained the project overview to us. We also utilized AI to write code and design algorithms.

# Description
　このプロジェクトでは以下のことを行います。<br>
・config.txtに記載された情報に基づいてランダムに迷路を作る。<br>
・迷路の中央に"42"の文字を入れる。迷路はこの文字を避けて作るようにする。<br>
・スタートとゴールの位置を表示し、スタートからゴールまでの最短経路を表示する。<br>
本プロジェクトでは、さらに不完全迷路で袋小路（三方が壁で囲まれた場所）をなくしています（42の文字の場所は除く）。<br>

## config.txtについて
このファイルは迷路生成のパラメータを設定します。<br>
WIDTH:迷路の横幅<br>
HEIGHT:迷路の縦幅<br>
PERFECT = Trueにすると完全迷路、Falseにすると不完全迷路が生成されます。<br>
ENTRY = スタート地点の座標<br>
OUTPUT_FILE = 生成した迷路のテキスト情報を格納するファイル。<br>
EXIT = ゴール地点の座標<br>
SEED = 乱数発生の元となる数値。SEEDの値が同じ場合、必ず同じ迷路が生成されます、ただし、同じSEED値でregenerateを選択すると別の迷路ができます。この迷路が生成される順番はSEED値が同じ場合必ず同一です。<br>



##　アルゴリズム

###　迷路生成方法<br>
　迷路生成は深さ優先探索（DFS）というアルゴリズムを使いました。この手法では、スタート地点から隣接する未訪問のマスへ移動し、移動した方向の壁を取り除いて通路を作ります。このアルゴリズムを本プロジェクトのコードに沿って以下説明します。<br>
１．全てのマスを壁で初期化する(line 175-178)。<br>
２．４２の文字を配置する(line 179,181)。<br>
３．訪問済みマスを管理する(line 183-186)。<br>
４．スタート地点からDFSを開始する(line 196,197)。<br<>
５．隣接する未訪問マスを探す(line 202-209)。<br>
６．ランダムに1つ選んで壁を取り除く(line 212-214)。<br>
７．移動先を訪問済みにしてスタックに追加する(line 215,216)。<br>
８．行き止まりになったら戻る(line 217,218)。<br>

　迷路生成の他のアルゴリズムとして有名なものに穴掘り法というのがあります。この手法では、スタート地点から穴を掘って未訪問の箇所を2マスずつ進みます。そのため、迷路の大きさは縦、横ともに奇数でなければならず、config.txtで縦あるいは横の大きさが偶数になった場合に対応できないため、本プロジェクトに適用するのに困難であると考えたため、上記のDFSを採用しました。

###　迷路探索方法<br>
　迷路の最短経路探索には幅優先探索（BFS）という手法を用いました。この手法以下の手順で最短経路を探します。<br>
1.スタート地点から始めて、1マス動ける場所を探します。複数あったら複数の場所を辞書に登録します。<br>
2.次に動けるマスを探します。これも複数あったら複数登録します。例えば1回目の移動で2箇所みつかり、そのそれぞれが次の移動で2箇所動ける場合、2回めの移動では合計4箇所が登録されることになります。<br>
3.ゴールが見つかったらそこで処理を終了します。複数ある経路の中のいずれかでゴールが見つかったら処理が終了するので、一番最初にゴールが見つかった経路が最短経路となります。<br>
4.辞書に記録された情報をたどり最短経路を復元します。<br>
　他の最短経路探索方法として、エースター探索というのがあります。この方法は迷路が大きい場合にはBFSより早く探索できるのですが、アルゴリズムが難解で、今回のプロジェクトのような小さい迷路であればBFSで十分であると判断しました。<br>

##　役割分担<br>
msumiji：README.mdの作成、コードの確認、修正<br>
ssagano：全体的なコードの作成、LICENSE.mdの作成<br>

##　プロジェクトを通しての感想
　チーム結成は8月に行いました。しかし、本プロジェクトは仮想環境を使うということでしたので、メンバーのうちどちらかがpython08を終わってから行うという方針にし、実際の着手は10月後半になってからです。当初はmsumijiの方が先にpython08を終わらせたので、msumijiがコードの作成の主担当とする予定でしたが、ssaganoの方が仮想環境の理解ができていたので、コードの作成の主担当はssaganoの方が行うことになりました。
　袋小路（dead-end）を消すことと、3×3のオープンスペースを作らないことを両立させるところは苦労しました。3方が塞がっている袋小路は3個の壁のどれかをランダムに選んで1つを消すというアルゴリズムにしたのですが、このときに3×3のオープンスペースができないかを検討しました。図面を書いて、袋小路が重なっている場所でどれか1つの壁を取り除いてもオープンスペースができる例が考えにくいことや、実際に不完全迷路を作ってみてオープンスペースができないことから、厳密な証明ができなくてもオープンスペースはできないものとしました。

#　良かった点と改善すべき点
　改善すべき点としては、最短経路のルートをわかりやすくすること。現状は単に点で示していますが、矢印で示してわかりやすくするとなお良かったと思います。さらには、迷路の経路を動画にして、再生するとスタートからゴールまで到達するようにするとなお良かったと思います。

## 利用した特別なツール
　また、本プロジェクトでは、仮想環境を使うことが強く推奨されていましたが、本プロジェクトではpythonの標準ライブラリのみを使ったので仮想環境を使う意味はなかったと思います。

# Instruction
make install:仮想環境をインストールする。他のコマンドを実行する場合はまずこれを実行します。

make run:プログラムを実行する。実行すると迷路が表示される。同時に4つの選択肢も表示される。それぞれの数字を入力することで、選択肢の内容が実行される。1を選択すると、別の迷路が生成される。SEED値が固定されている場合は、必ず同じ順番で別の迷路が表示される仕組みになっている。例えば、SEED=42に設定している場合、Re-generate a new mazeを選択することで、迷路A→迷路B→迷路Cのように迷路が作られるが、SEED=41にすると、迷路D→迷路E→迷路Fの順番に作られます。

make debug:pythonに標準に備えられているデバッガーpdbを使う。これを使うとプログラムを1行だけ実行することができます。

make clean:仮想環境やmypy_cacheなどの一時的に作られたファイルを削除します。

make lint:flake8とmypyのチェックを行う。make lint-strictにすると、flake8と同時にmypy --strict .を実行します。

## Code Reusability
　本プロジェクトの迷路プログラムは、独立した再利用可能なモジュール（`mazegen`）として実装されており、将来のプロジェクトにインポートして使用することができます。例えば本プロジェクトの迷路プログラムをパックマンゲームに利用する場合を考えます。この場合、迷路の描画に関する箇所とインタラクティブメニューの表示以外の箇所は再利用.venv)することができます。具体的には、MazeGeneratorクラスのrender,export,run_interactiveメソッドの部分です。以下本プログラムをインポートする方法を解説します。

### 1. パッケージのビルド方法
Makefile の `install` 規則を実行すると、仮想環境内にwheel` パッケージが自動的にビルドされます。これを利用して、以下のコマンドでパッケージをビルドし、`.whl` ファイルを生成できます。

#### 依存関係のインストール（build と wheel が含まれます）
make install

#### 仮想環境を有効化してパッケージをビルド
make build

ビルドが成功すると、ルート直下に dist/ ディレクトリが作成され、Wheel ファイルが生成されます。
生成例: dist/mazegen-1.0.0-py3-none-any.whl

### ２. パッケージのインストールと使用方法
生成された .whl ファイルは、pip を用いて任意の仮想環境やプロジェクトにインストールできます。
pip install dist/mazegen-1.0.0-py3-none-any.whl

## Resources
　このプロジェクトを作成するにあたって、同期入学の学生からの助言を利用しました。たまたまa_maze_ingのレビューをする機会がたくさんあり、その機会にa_maze_ingのプロジェクトの概要を教えてもらいました。また、コードの作成、アルゴリズムの構築にはAIを活用しました。
