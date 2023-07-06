# Create the colgroup element
colgroup = soup.new_tag('colgroup')

# Create and append the col elements with specific widths
colgroup.append(soup.new_tag('col', style='width: 4%;'))
colgroup.append(soup.new_tag('col', style='width: 2%;'))
colgroup.append(soup.new_tag('col', style='width: 8%;'))
colgroup.append(soup.new_tag('col', style='width: 10%;'))
colgroup.append(soup.new_tag('col', style='width: 10%;'))
colgroup.append(soup.new_tag('col', style='width: 2%;'))
