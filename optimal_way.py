import optimal_way_util

def which_side_points(a, b, c):
    d = (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])
    return 1 if d > 0 else (-1 if d < 0 else 0)


def is_point_in_closed_segment(a, b, c):
    if a[0] < b[0]:
        return a[0] <= c[0] <= b[0]
    if b[0] < a[0]:
        return b[0] <= c[0] <= a[0]

    if a[1] < b[1]:
        return a[1] <= c[1] <= b[1]
    if b[1] < a[1]:
        return b[1] <= c[1] <= a[1]

    return a[0] == c[0] and a[1] == c[1]


def segment_intersection(a, b, c, d):
    if a == b:
        return a == c or a == d
    if c == d:
        return c == a or c == b

    s1 = which_side_points(a, b, c)
    s2 = which_side_points(a, b, d)

    if s1 == 0 and s2 == 0:
        return \
            is_point_in_closed_segment(a, b, c) \
            or is_point_in_closed_segment(a, b, d) \
            or is_point_in_closed_segment(c, d, a) \
            or is_point_in_closed_segment(c, d, b)

    if s1 and s1 == s2:
        return False

    s1 = which_side_points(c, d, a)
    s2 = which_side_points(c, d, b)

    if s1 and s1 == s2:
        return False

    return True


def which_side(line, point):
    return (point[0] - line[0][0]) * (line[1][1] - line[0][1]) - (point[1] - line[0][1]) * (line[1][0] - line[0][0])

def object_control(start, end, konvexne_obalky):
    relevant_objects = []
    for i in konvexne_obalky:
        object = i
        priesecnik = []
        for j in range(len(object) - 1):
            point_1 = object[j]
            point_2 = object[j + 1]
            if start == point_1 or start == point_2:  # neberie do uvahy stranu v ktorej sa nachadza start
                continue
            if segment_intersection(point_1, point_2, start, end):
                priesecnik.append(1)

        if len(priesecnik) > 0:
            relevant_objects.append(i)

    return relevant_objects


def optimal_way(start, end, konvexne_obalky):
    for obstacle in konvexne_obalky:
        obstacle.pop(-1)

    path = [start]

    while not path[-1] == end:
        relevant_objects = object_control(start, end, konvexne_obalky)

        if len(relevant_objects) == 0:
                path.append(end)

        else:
            closest_point, closest_object = optimal_way_util.get_closest_point(relevant_objects, start)
            for point in closest_object:
                line = [start, end]
                det = which_side(line, point)
                if det > 0:
                    point.append(1)
                else:
                    point.append(-1)

            sign = closest_point[-1]                #na ktorej strane je closest_point
            closest_point.pop(-1)
            if closest_point not in path:
                path.append(closest_point)

            points = []
            for point in closest_object:
                if point == closest_point:
                    pass
                elif point[-1] == sign:             #ak sa strany zhoduju, prida point do cesty
                    point.pop(-1)
                    points.append(point)
                else:
                    point.pop(-1)

            index = closest_object.index(closest_point)

            for point in points:
                if index == 0:
                    if point == closest_object[1] or point == closest_object[-1]:
                        path.append(point)
                elif index == len(closest_object) - 1:
                    if point == closest_object[-2] or point == closest_object[0]:
                        path.append(point)
                elif point == closest_object[index + 1] or point == closest_object[index - 1]:
                    path.append(point)
                else:
                    pass
            start = path[-1]
    return path