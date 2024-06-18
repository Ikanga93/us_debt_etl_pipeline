# Define the mapping of years to presidents

president_mapping = {
    range(1789, 1797 + 1): "GEORGE WASHINGTON",
    range(1797, 1801 + 1): "JOHN ADAMS",
    range(1801, 1809 + 1): "THOMAS JEFFERSON",
    range(1809, 1817 + 1): "JAMES MADISON",
    range(1817, 1825 + 1): "JAMES MONROE",
    range(1825, 1829 + 1): "JOHN QUINCY ADAMS",
    range(1829, 1837 + 1): "ANDREW JACKSON",
    range(1837, 1841 + 1): "MARTIN VAN BUREN",
    range(1841, 1841 + 1): "WILLIAM HENRY HARRISON",
    range(1841, 1845 + 1): "JOHN TYLER",
    range(1845, 1849 + 1): "JAMES K. POLK",
    range(1849, 1850 + 1): "ZACHARY TAYLOR",
    range(1850, 1853 + 1): "MILLARD FILLMORE",
    range(1853, 1857 + 1): "FRANKLIN PIERCE",
    range(1857, 1861 + 1): "JAMES BUCHANAN",
    range(1861, 1865 + 1): "ABRAHAM LINCOLN",
    range(1865, 1869 + 1): "ANDREW JOHNSON",
    range(1869, 1877 + 1): "ULYSSES S. GRANT",
    range(1877, 1881 + 1): "RUTHERFORD B. HAYES",
    range(1881, 1881 + 1): "JAMES A. GARFIELD",
    range(1881, 1885 + 1): "CHESTER A. ARTHUR",
    range(1885, 1889 + 1): "GROVER CLEVELAND",
    range(1889, 1893 + 1): "BENJAMIN HARRISON",
    range(1893, 1897 + 1): "GROVER CLEVELAND",
    range(1897, 1901 + 1): "WILLIAM MCKINLEY",
    range(1901, 1909 + 1): "THEODORE ROOSEVELT",
    range(1909, 1913 + 1): "WILLIAM HOWARD TAFT",
    range(1913, 1921 + 1): "WOODROW WILSON",
    range(1921, 1923 + 1): "WARREN G. HARDING",
    range(1923, 1929 + 1): "CALVIN COOLIDGE",
    range(1929, 1933 + 1): "HERBERT HOOVER",
    range(1933, 1945 + 1): "FRANKLIN D. ROOSEVELT",
    range(1945, 1953 + 1): "HARRY S. TRUMAN",
    range(1953, 1961 + 1): "DWIGHT D. EISENHOWER",
    range(1961, 1963 + 1): "JOHN F. KENNEDY",
    range(1963, 1969 + 1): "LYNDON B. JOHNSON",
    range(1969, 1974 + 1): "RICHARD M. NIXON",
    range(1974, 1977 + 1): "GERALD R. FORD",
    range(1977, 1981 + 1): "JIMMY CARTER",
    range(1981, 1989 + 1): "RONALD REAGAN",
    range(1989, 1993 + 1): "GEORGE BUSH",
    range(1993, 2001 + 1): "WILLIAM J. CLINTON",
    range(2001, 2009 + 1): "GEORGE W. BUSH",
    range(2009, 2017 + 1): "BARACK OBAMA",
    range(2017, 2021 + 1): "DONALD J. TRUMP",
    range(2021, 2024 + 1): "JOSEPH R. BIDEN JR."
}

# Create a dictionary to map each year to the corresponding president
year_to_president = {}
for years, president in president_mapping.items():
    for year in years:
        year_to_president[year] = president