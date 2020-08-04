
import pandas as pd

age = pd.Series([10,12,13], index=list('ABC'))
gender = pd.Series(list('MFF'), index=list('ABC'))
curr_df = pd.DataFrame({
    'Age': age,
    'Gender': gender
})
name = pd.Series(['Ana', 'Python', 'Robert', "Olivia"], index=list('ABXD'))
curr_df['name'] = name
print(curr_df)
# ^ This will be missing D row because not in original index
new_df = pd.DataFrame({
    'Age': age,
    'Gender': gender,
    'name': name
})
# ^ This will contain D row because created new index on the DataFrame's creation from the primitive `dict`
print(new_df)