def calculate_helical_positions(self, pos1, pos2, osc_start, osc_range, overlap, number_images, shifts):
      positions = []
      phi_start = osc_start
      phi_stop = osc_start + (osc_range - overlap) * (number_images - 1)
      phi_range = phi_start - phi_stop
      d_phi = math.fabs(float(phi_range)) / shifts
      phiy_range = float(pos1["phiy"]) - float(pos2["phiy"])

      hp1 = { "sampx": (float(pos1["sampx"]) - float(pos2["sampx"])) / phiy_range,
              "sampy": (float(pos1["sampy"]) - float(pos2["sampy"])) / phiy_range,
              "phiz": (float(pos1["phiz"]) - float(pos2["phiz"])) / phiy_range,
              "phiy": phiy_range / phi_range }
      hp2 = { "sampx": ((float(pos1["phiy"]) * float(pos2["sampx"])) - (float(pos2["phiy"]) * float(pos1["sampx"]))) / phiy_range,
              "sampy": ((float(pos1["phiy"]) * float(pos2["sampy"])) - (float(pos2["phiy"]) * float(pos1["sampy"]))) / phiy_range,
              "phiz": ((float(pos1["phiy"]) * float(pos2["phiz"])) - (float(pos2["phiy"]) * float(pos1["phiz"]))) / phiy_range,
              "phiy": ((osc_start * float(pos2["phiy"])) - (phi_stop * float(pos1["phiy"]))) / phi_range  }

      phi_pos = osc_start
      for i in range(shifts):
        phiy = hp1["phiy"] * phi_pos + hp2["phiy"]
        phiz = hp1["phiz"] * phiy + hp2["phiz"]
        sampx = hp1["sampx"] * phiy + hp2["sampx"]
        sampy = hp1["sampy"] * phiy + hp2["sampy"]

        positions.append({ "phi": phi_pos,
                           "phiy": phiy,
                           "phiz": phiz,
                           "sampx": sampx,
                           "sampy": sampy })

        phi_pos += d_phi

      return positions

