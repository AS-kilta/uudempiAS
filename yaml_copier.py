'''

Quick and really dirty script for copying data between two YAMLs for different languages.
No error handling, you can really mess up something in the target file with this.
For this to work, the parameters have to be in the same row in both files.

This was written at 4 AM in a couple of minutes and it pretty much looks like it.

TODO: smarter tool for the purpose (if someone has time or interest)...

'''

def main():
    with open("_data/toimarit.yaml", "r") as f:
        src = f.readlines()
    with open("_data/toimarit_en.yaml", "r") as f:
        dst = f.readlines()
    dstrow = 0
    for srcrow in src:
        if "picture:" in srcrow:
            dst[dstrow] = srcrow
        dstrow += 1
    with open("_data/toimarit_en.yaml", "w") as f:
        f.writelines(dst)
    return

main()
        