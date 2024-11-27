import torch

class TurkeyNN(torch.nn.Module):

    def __init__(self, hid_size, sec_num):

        super().__init__()
        self.gru = torch.nn.GRU(1, hid_size)
        self.lin = torch.nn.Linear(hid_size, sec_num)
        self.prob = torch.nn.LogSoftmax(dim=-1)
        self.crit = torch.nn.CrossEntropyLoss()

    def forward(self, in_tens):

        out, _ = self.gru(in_tens)
        
        out = out[-1,:].unsqueeze(0)

        probs = self.prob(self.lin(out))

        return probs
    
    def updateModel(self, probs, inf_sec, optimizer):

        optimizer.zero_grad()
        loss = self.crit(probs, inf_sec)
        loss.backward()
        optimizer.step()
