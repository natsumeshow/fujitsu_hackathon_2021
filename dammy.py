import numpy as np

def model(image, e, resize_to_default=(True, True), upsample_size=4):
    t = 0.2
    v = np.random.rand(18)
    return {i: np.random.randint(0,200,(2)).tolist() for i in range(18) if v[i]>t}

if __name__ == "__main__":
    print(model(0, 0, resize_to_default=(True, True), upsample_size=4))