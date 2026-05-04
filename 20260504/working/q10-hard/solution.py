def build_team_members(n, team_ids):
    team_members = {}

    for employee_id in range(1, n + 1):
        team_id = team_ids[employee_id]

        if team_id not in team_members:
            team_members[team_id] = []

        team_members[team_id].append(employee_id)

    return team_members


def remove_employee(employee_id, efficiencies, alive):
    if not alive[employee_id]:
        return 0

    alive[employee_id] = False
    return efficiencies[employee_id]


def remove_lowest_alive_from_team(team_id, team_members, efficiencies, alive):
    members = team_members[team_id]
    chosen_employee = 0
    chosen_efficiency = 0

    for employee_id in members:
        if not alive[employee_id]:
            continue

        efficiency = efficiencies[employee_id]

        if chosen_employee == 0:
            chosen_employee = employee_id
            chosen_efficiency = efficiency
        elif efficiency < chosen_efficiency:
            chosen_employee = employee_id
            chosen_efficiency = efficiency
        elif efficiency == chosen_efficiency and employee_id < chosen_employee:
            chosen_employee = employee_id
            chosen_efficiency = efficiency

    if chosen_employee == 0:
        return 0

    alive[chosen_employee] = False
    return chosen_efficiency


def get_reputation_after_each_day(n, efficiencies_list, team_ids_list, queries):
    efficiencies = [0] + efficiencies_list
    team_ids = [0] + team_ids_list
    alive = [True] * (n + 1)

    team_members = build_team_members(n, team_ids)
    reputation = sum(efficiencies_list)
    answers = []

    for fire_id, resign_count in queries:
        reputation -= remove_employee(fire_id, efficiencies, alive)

        team_id = team_ids[fire_id]
        for _ in range(resign_count):
            reputation -= remove_lowest_alive_from_team(
                team_id, team_members, efficiencies, alive
            )

        answers.append(reputation)

    return answers


def solve():
    n = int(input())
    efficiencies = list(map(int, input().split()))

    num_t = int(input())
    team_ids = list(map(int, input().split()))

    q, num_e = map(int, input().split())

    queries = []
    for _ in range(q):
        fire_id, resign_count = map(int, input().split())
        queries.append((fire_id, resign_count))

    answers = get_reputation_after_each_day(n, efficiencies, team_ids, queries)
    print(*answers)


if __name__ == "__main__":
    solve()
