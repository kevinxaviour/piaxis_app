def find_best_match(rules, request):
    best_score = 0
    best_rule = None

    for rule in rules:
        score = 0

        if rule.host_element.lower() == request.host_element.lower():
            score += 1
        if rule.adjacent_element.lower() == request.adjacent_element.lower():
            score += 1
        if rule.exposure.lower() == request.exposure.lower():
            score += 1

        if score > best_score:
            best_score = score
            best_rule = rule

    return best_rule, best_score