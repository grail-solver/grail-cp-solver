prompt_equation = """
Format this equation "<equation>" following this example:

input:
Constraints:{"eq1":"Var_1>=1","eq2":"(1/2)Var_1<=10", "eq3":"Var_1+2*Var_2-50*Var_3=1000"}

output:
"constraints": [
    {
        "left_part": [
          [
            1,
            "Var_1"
          ]
        ],
        "relation": ">=",
        "right_part": [
          1
        ]
    },
    {
        "left_part": [
          [
            1/2,
            "Var_1"
          ]
        ],
        "relation": "<=",
        "right_part": [
          10
        ]
    },
    {
        "left_part": [
          [
            1,
            "Var_1"
          ],
          "+",
          [
            2,
            "Var_2"
          ],
          "-",
          [
            50,
            "Var_3"
          ],
        ],
        "relation": "=",
        "right_part": [
          1000
        ]
    }
]

Important: The output must be valid string i can parse directly in json. Do not add comment.
"""